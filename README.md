Django Unused Context
=====================

Django Middleware providing a mechanism for triggering warnings about template
context keys that do not get used while rendering the template.

Full documentation on [read the docs](https://django-unused-context.readthedocs.io/en/latest/index.html).


## Installation

1. Install the package:
```shell
python -m pip install django-unused-context
```

<br>

2. Add the middleware to your Django `settings.py` file:
```python
MIDDLEWARE = [


    'django_unused_context.middleware.UnusedContextMiddleware',

    ...
]
```

<br>

3. Ensure that `DEBUG` is set to `True` in your Django settings file.
```python
DEBUG = True
```

## Usage

Usage is automatic once the middleware is added. On each response that renders
a template, any variables that were added to the template's context and then
not used in the template rendering will be added to an internal set that will
be both logged out and raise warnings. This is useful for knowing that all
variables being sent to a template are being used.

## Configuration
The package has a couple of configuration options available to you.
The options can be set by adding the associated option and its value into
your settings file for Django.

### DJANGO_UNUSED_CONTEXT_ALWAYS
Default: ```False```<br>
The tool will only show warnings and log out messages when the project's
settings has `DEBUG = True`. If you would like to have unused context variables
logged out and raise warnings regardless of whether `DEBUG = True`, set this
setting to `True`.

This is useful for having tests output any unused context variables.
Since tests are normally run with `DEBUG` set to `False`, you will never see
output from this tool when running tests. If you would like to see this output
when running tests as well you can, set this setting to `True`.

**NOTE:** It is strongly Encouraged that you do NOT turn this setting on for a
project that is in production as it will slow down the site and do unnecessary
logging.

```python
DJANGO_UNUSED_CONTEXT_ALWAYS = True
```

### DJANGO_UNUSED_CONTEXT_IGNORE
Default: ```[]``` (Empty List)<br>
The tool comes with some default keys that are automatically ignored regardless
of whether they are used or not in a template. Many of these are provided by
Django automatically and thus often times may not be used in a template.
Rather than constantly seeing these, it seemed more reasonable to ignore them.

The predefined keys to ignore include:

```python
'block',                  # block.super not called in overridden template.
'csrf_token',             # Given to all templates.
'DEFAULT_MESSAGE_LEVELS', # Given to all templates using messages framework.
'False',                  # Given to all templates.
'forloop',                # Given to templates with a for loop.
'is_paginated',           # Included by ListView and may not need pagination.
'None',                   # Given to all templates.
'page_obj',               # Included by ListView and may not need pagination.
'paginator',              # Included by ListView and may not need pagination.
'perms',                  # Given to login_required templates.
'root_urlconf',           # Given to exception pages for 404.
'settings',               # Likely to be given to templates and not used.
'site',                   # Given to the login page and may not be used.
'site_name',              # Given to the login page and may not be used.
'True',                   # Given to all templates.
'view',                   # Given to built-in password reset page.
```

If you would like to add additional keys to ignore that are specific to your
project, you can do that here.
Be sure to list each key in the list as a string.
```python
DJANGO_UNUSED_CONTEXT_IGNORE = [
    'errors'
]
```
