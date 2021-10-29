import uuid

from django.apps import apps
from django.db import models
from django.test import TestCase, override_settings
from django.utils import timezone
from pathlib import Path

from .apps import JsonSchemaGeneratorConfig
from .schemas import Schema


APP_TO_INSTALL = [
    'json_schema_generator.apps.JsonSchemaGeneratorConfig',
]
APP_NAME = JsonSchemaGeneratorConfig.name
PATH_TEST = '/tmp'
FILENAME = 'django_schema.json'


# -- Define Models for tests only ---------------
class ModelA(models.Model):
    name = models.CharField('Name', max_length=150, null=False, blank=False)


class ModelB(models.Model):
    number = models.IntegerField('Number', null=False, blank=False)


class SimpleModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    char = models.CharField('Char', max_length=100, null=False, blank=False)
    integer = models.IntegerField('Integer', null=False, blank=False)
    boolean = models.BooleanField('Boolean', default=True,
                                  null=False, blank=False)
    text_nullable = models.TextField('Text', null=True, blank=False)
    date_creation = models.DateTimeField('Creation date',
                                         default=timezone.now,
                                         null=False, blank=False)


class RefModel(models.Model):
    one_to_one = models.OneToOneField(ModelA, on_delete=models.CASCADE)
    foreign_key = models.ForeignKey(SimpleModel, on_delete=models.CASCADE,
                                    related_name='fks',
                                    null=False, blank=False)
    many_to_many = models.ManyToManyField(ModelB, blank=True)
# -----------------------------------------------


class SchemaTest(TestCase):
    @override_settings(INSTALLED_APPS=APP_TO_INSTALL)
    def test_get_app_configs(self):
        app_configs = list(apps.get_app_configs())
        self.assertEqual(len(app_configs), 1)
        self.assertEqual(app_configs[0].name, APP_NAME)

    @override_settings(INSTALLED_APPS=APP_TO_INSTALL)
    def test_get_apps(self):
        res = Schema().get_apps()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['application'], APP_NAME)
        self.assertGreater(len(res[0]['models']), 1)

    @override_settings(INSTALLED_APPS=APP_TO_INSTALL)
    def test_get_models(self):
        app = apps.get_app_config(APP_NAME)
        res = Schema().get_models(app)
        self.assertEqual(
            set(['ModelA', 'ModelB', 'SimpleModel', 'RefModel']),
            set([model['name'] for model in res])
        )

    def test_get_fields(self):
        model = SimpleModel()
        res = Schema().get_fields(model)
        self.assertEqual(
            set(['id', 'char', 'integer', 'boolean', 'text_nullable',
                 'date_creation', 'fks']),
            set([field['name'] for field in res])
        )

    def test_primary_key(self):
        model = SimpleModel()
        res = Schema().get_fields(model)
        all_primary_keys = [field['name'] for field in res
                            if 'primary_key' in field]
        self.assertEqual(len(all_primary_keys), 1)
        self.assertEqual(all_primary_keys[0], 'id')

    def test_nullable(self):
        model = SimpleModel()
        res = Schema().get_fields(model)
        all_nullable = [field['name'] for field in res
                        if 'relation' not in field and field['nullable']]
        self.assertEqual(len(all_nullable), 1)
        self.assertEqual(all_nullable[0], 'text_nullable')

    def test_max_length(self):
        model = ModelA()
        res = Schema().get_fields(model)
        all_max_length = [field for field in res if 'max_length' in field]
        self.assertEqual(len(all_max_length), 1)
        self.assertEqual(all_max_length[0]['name'], 'name')
        self.assertEqual(all_max_length[0]['max_length'], 150)

    def test_default_value(self):
        model = SimpleModel()
        res = Schema().get_fields(model)
        all_default = [field for field in res if 'default' in field]
        self.assertEqual(len(all_default), 1)
        self.assertEqual(all_default[0]['name'], 'boolean')
        self.assertEqual(all_default[0]['default'], True)

    def test_default_func(self):
        model = SimpleModel()
        res = Schema().get_fields(model)
        all_default_func = [field for field in res if 'default_func' in field]
        self.assertEqual(len(all_default_func), 2)
        self.assertEqual(all_default_func[0]['name'], 'id')
        self.assertEqual(all_default_func[0]['default_func'], 'uuid.uuid4()')

    def test_get_relation(self):
        model = RefModel()
        res = Schema().get_fields(model)
        all_relations = [field for field in res if 'relation' in field]
        self.assertEqual(len(all_relations), 3)

    @override_settings(SCHEMA_GENERATOR_DIRECTORY=PATH_TEST)
    @override_settings(SCHEMA_GENERATOR_FILENAME=FILENAME)
    def test_file_creation_after_generate(self):
        Schema().generate()
        path_file = Path(PATH_TEST) / Path(FILENAME)
        self.assertTrue(path_file.exists())
        path_file.unlink()
