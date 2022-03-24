Django Unused Context
============================

Django App providing a mechanism for triggering warnings about variables sent to
a template context that are not used in the template.


## Installation
Import the package via either:
```shell
python -m pip install -e "git+https://github.com/DJBarnes/django-unused-context#egg=django-unused-context"
```
or
```shell
pipenv install -e "git+https://github.com/DJBarnes/django-unused-context#egg=django-unused-context"
```

<br>

Next add the corresponding app to your Django `settings.py` file:
```python
INSTALLED_APPS = [
    ...

    'django_unused_context',

    ...
]
```

<br>

Lastly add the corresponding middleware to your Django `settings.py` file:
```python
MIDDLEWARE = [
    ...

    'django_unused_context.middleware.UnusedContextMiddleware',

    ...
]
```

## Usage
TODO: Fill out.

## Configuration
The package has a few configuration options available to you. Each of the following options can be set by adding the associated option and value into your settings file for Django.

### DJANGO_UNUSED_CONTEXT_IGNORE
Default: ```[]``` (Empty List)<br>
The tool comes with some default variables that are passed to every single template regardless and thus are ignored as often times they will never be used.
Predefined variables to ignore include:
* 'None'
* 'False'
* 'True'

If you would like to add additional variables to ignore that are specific to your project, you can do that here.
Be sure to list each variable in the list as a string of the variable to ignore.
```python
DJANGO_UNUSED_CONTEXT_IGNORE = [
    'paginator'
]
```
