Quickstart
==========

1. Install the Django App via GitHub for now. Working on getting on Pypi soon.
    .. code-block:: bash

        python -m pip install -e git+https://github.com/DJBarnes/django-unused-context@master


2. Add the corresponding app to your Django ``settings.py`` file:
    .. code-block:: python

        INSTALLED_APPS = [

            'django_unused_context',
            ...
        ]


3. Add the corresponding middleware to your Django ``settings.py`` file:
    .. code-block:: python

        MIDDLEWARE = [


            'django_unused_context.middleware.UnusedContextMiddleware',
            ...
        ]

4. Ensure that you have ``DEBUG`` set to ``True`` in your Django
   ``settings.py`` file:

    .. code-block:: python

        DEBUG = True

5. Usage is automatic once the middleware is added. On each response that
   renders a template, any variables that were added to the template's context
   and then not used in the template rendering will be added to an internal set
   that will be both logged out and raise warnings. This is useful for knowing
   that all variables being sent to a template are being used.



See the :doc:`configuration` section for more information on customizing how
django-unused-context operates.
