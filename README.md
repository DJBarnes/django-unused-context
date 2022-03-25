Django Unused Context
============================

Django App providing a mechanism for triggering warnings about context keys for
a template that are not used.


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
The package has one configuration option available to you. The following option can be set by adding the associated option and value into your settings file for Django.

### DJANGO_UNUSED_CONTEXT_IGNORE
Default: ```[]``` (Empty List)<br>
The tool comes with some default keys that are included in every single template regardless and thus are ignored as often times they will never be used.
Predefined keys to ignore include:
* 'None'
* 'False'
* 'True'

If you would like to add additional keys to ignore that are specific to your project, you can do that here.
Be sure to list each key in the list as a string.
```python
DJANGO_UNUSED_CONTEXT_IGNORE = [
    'paginator'
]
```
