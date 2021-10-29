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

### File structure

* **`Root`**: a list of `App` object
* **`App`**
    * **application**: app name
    * **models**: a list of `Model` object
* **`Model`**
    * **name**: model name 
    * **db_table**: the name of database table
    * **fields**: list of `Field` object
* **`Field`**
    * **name**: field name
    * **django_type**: Django type of the field
    * **nullable**: it defines if it's nullable field or not
    * **max_length**: *[occasional]* it defines the max length of the field
    * **primary_key**: *[occasional]* it defines if it's the primary key field
    * **default**: *[occasional]* it defines the static default value
    * **default_func**: *[occasional]* it defines the method which used for the default value
    * **relation**: *[occasional]* a `Relation` object if it's a relation field
* **`Relation`**
    * **one_to_one**: it defines if it's an one_to_one relation
    * **one_to_many**: it defines if it's an one_to_many relation
    * **many_to_one**: it defines if it's a many_to_one relation
    * **many_to_many**: it defines if it's a many_to_many relation

### An example
```json
[
{
    "application": "my_app",
    "models": [
    {
        "name": "MyModel",
        "db_table": "my_app_mymodel",
        "fields": [
        {
            "name": "id",
            "django_type": "UUIDField",
            "nullable": false,
            "max_length": 32,
            "primary_key": true,
            "default_func": "uuid.uuid4()"
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
            "default": true
        },
        {
            "name": "many_to_many",
            "django_type": "ManyToManyField",
            "nullable": false,
            "relation":
            {
                "one_to_one": false,
                "one_to_many": false,
                "many_to_one": false,
                "many_to_many": true
            }
        }]
    },
    ]
},
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
