from django.apps import AppConfig


class JsonSchemaGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'json_schema_generator'

    def ready(self):
        from .schemas import Schema
        Schema().generate()
