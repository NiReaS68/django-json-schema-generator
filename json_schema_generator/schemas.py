import json
from django.apps import apps
from django.conf import settings
from pathlib import Path


class Schema(object):
    def __init__(self, *args, **kwargs):
        self.schema = []

    def generate(self, save_file=True):
        """
        Entry point for the schema generator
        """
        self.schema = self.get_apps()
        if save_file:
            self.write_file()

    def get_apps(self):
        """
        Return the list of all installed applications with all models
        """
        app_list = []
        for app in apps.get_app_configs():
            app_list.append({
                'application': app.name,
                'models': self.get_models(app)
            })
        return app_list

    def get_models(self, app):
        """
        Return the models list in the application with some options and
        all fields
        """
        model_list = []
        for model in app.get_models():
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
            options = {
                'name': field.name,
                'django_type': field.get_internal_type(),
                'nullable': field.null,
            }
            if hasattr(field, 'max_length') and field.max_length:
                options['max_length'] = field.max_length
            if hasattr(field, 'primary_key') and field.primary_key:
                options['primary_key'] = field.primary_key
            if hasattr(field, 'has_default') and field.has_default():
                if hasattr(field.default, '__call__'):
                    options['default_func'] = (f"{field.default.__module__}."
                                               f"{field.default.__name__}()")
                else:
                    options['default'] = field.default

            if field.is_relation:
                options['relation'] = self.get_relation(field)

            field_list.append(options)
        return field_list

    def get_relation(self, field):
        """
        Return the dict of the relation options of the field
        """
        # TODO: add field.through._meta.db_table for many_to_many relation
        return {
            'one_to_one': field.one_to_one,
            'one_to_many': field.one_to_many,
            'many_to_one': field.many_to_one,
            'many_to_many': field.many_to_many,
        }

    def write_file(self):
        """
        TODO: add format choices, the yaml format for example, but change the
        app name for more coherence (remove "json"). It can be a parameter
        of this method or a new setting:
            getattr(settings, 'SCHEMA_GENERATOR_FORMAT', 'json')
        """
        directory = getattr(settings, 'SCHEMA_GENERATOR_DIRECTORY',
                            str(Path.cwd()))
        filename = getattr(settings, 'SCHEMA_GENERATOR_FILENAME',
                           '.forestadmin-schema.json')
        path = str(Path(directory) / Path(filename))

        with open(path, 'w') as f:
            json.dump(self.schema, f)

    # TODO get_constraints(self, field)
