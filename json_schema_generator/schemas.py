import json
from django.apps import apps
from django.conf import settings
from pathlib import Path


class Schema(object):
    def __init__(self, *args, **kwargs):
        self.schema = []
        self.stats = {
            'apps': 0,
            'models': 0,
            'db_tables': 0,
            'fields': 0,
            'indexes': 0,
            'relations': 0,
        }

    def generate(self, save_file=True):
        """
        Entry point for the schema generator
        """
        for app in apps.get_app_configs():
            self.stats['apps'] += 1
            self.schema.append({
                'application': app.name,
                'models': self.get_models(app)
            })

        if save_file:
            self.write_file()
        print(self.stats)

    def get_models(self, app):
        """
        Return the models list of the django application with some options
        """
        model_list = []
        for model in app.get_models():
            self.stats['models'] += 1
            self.stats['db_tables'] += 1
            model_list.append({
                'name': model.__name__,
                'db_table': model._meta.db_table,
                'fields': self.get_fields(model),
            })
        return model_list

    def get_fields(self, model):
        """
        Return the list of all fields in the model with some options
        into a dict
        """
        field_list = []
        for field in model._meta.get_fields():
            self.stats['fields'] += 1
            options = {
                'name': field.name,
                'django_type': field.get_internal_type(),
                'nullable': field.null,
            }
            if hasattr(field, 'has_default') and field.has_default():
                if hasattr(field.default, '__call__'):
                    options['default_func'] = (f"{field.default.__module__}."
                                               f"{field.default.__name__}()")
                else:
                    options['default'] = field.default

            if hasattr(field, 'db_index') and field.db_index:
                options['index'] = field.db_index
                self.stats['indexes'] += 1

            if field.is_relation:
                options['relation'] = self.get_relation(field)

            field_list.append(options)
        return field_list

    def get_relation(self, field):
        """
        Return the dict of the relation options of the field
        """
        self.stats['relations'] += 1
        return {}

    def write_file(self):
        """
        TODO: add format choices, with yaml for example, but change the app
        name for more coherence (remove "json"). It can be a setting:
            getattr(settings, 'SCHEMA_GENERATOR_FORMAT', 'json')
        """
        directory = getattr(settings, 'SCHEMA_GENERATOR_PATH', str(Path.cwd()))
        filename = getattr(settings, 'SCHEMA_GENERATOR_FILENAME',
                           '.forestadmin-schema.json')
        path = str(Path(directory) / Path(filename))
        print(path)

        with open(path, 'w') as f:
            json.dump(self.schema, f)

    # TODO get_constraints(self, field)
