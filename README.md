# django-json-schema-generator

This app describes all models and fields on your project and generates a json file of the project schema on startup.

# Documentation
## How to use it ?

### Requirements

* Python >= 3.6
* Django >= 3.0
* A Django project

### Installation

1. Download the package or build from the source:

```sh
python setup.py sdist
```

*You can find the package into the `dist` directory.*

2. Install the package in your project. For example with `pip`

```sh
python -m pip install django-json-schema-generator-X.Y.tar.gz
````

3. To finish, add this app in your Django project

```python
INSTALLED_APPS = [
    ...,
    json_schema_generator
]
```

This app is now installed and the file generation will do on your Django project startup. 

### Configuration

You can set some options:

* **`SCHEMA_GENERATOR_DIRECTORY`**: Set the folder of the generated file *(default: at the root of the Django project)*
* **`SCHEMA_GENERATOR_FILENAME`**: Set the generated filename *(default: .forestadmin-schema.json)*

## How to read the schema file ?

The generated schema file is composed of the list of the all installed apps in your Django project. For each Django app you can find the list of models with some options and for each model you can find the list of fields and some options.

A example of the file structure:
```json
[
{
    "application": "my_app", // app name
    "models": [ // list of app models
    {
        "name": "MyModel", // model name
        "db_table": "my_app_mymodel", // the name of database table
        "fields": [ // list of model fields
        {
            "name": "id", // field name
            "django_type": "UUIDField", // Django type of the field
            "nullable": false, // it defines if it's nullable field or not
            "max_length": 32, // [optional] it defines the max length of the field
            "primary_key": true, // [optional] it defines if it's the primary key field
            "default_func": "uuid.uuid4()" // [optional] it defines the method which used for the default value
        },
        {
            "name": "name",
            "django_type": "CharField",
            "nullable": false,
            "max_length": 150
        },
        {
            "name": "activate",
            "django_type": "BooleanField",
            "nullable": false,
            "default": true // [optional] it defines the static default value
        },
        {
            "name": "many_to_many",
            "django_type": "ManyToManyField",
            "nullable": false,
            "relation": // [optional] it defines the relation properties
            {
                "one_to_one": false,
                "one_to_many": false,
                "many_to_one": false,
                "many_to_many": true
            }
        }]
    }, // other models
    ]
}, // other apps
]
```


### *TODO: what is missing ?*

* Add database type: convert the Django field to the database field
* Add more file formats for the generated file (example: yaml)
* Add more properties for the field relation: like the reference of field and the database table used for the ManyToManyField
* Add more tests
* Add the possibility to escape the Django apps introspection (admin, auth, ...)
* Add debug/info log messages (with statistics for example)
* Add the indexes management
* Add the constraints management
* Add the abstract model management
* Add the proxy model management
