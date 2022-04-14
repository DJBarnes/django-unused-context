"""
Middleware for Unused Context.
"""

import contextlib
import logging
import threading
import warnings

from django.conf import settings
from django.template import Context


# Set up logging.
logger = logging.getLogger('django_unused_context')
# Get additional keys to ignore.
django_unused_context_ignore = getattr(settings, 'DJANGO_UNUSED_CONTEXT_IGNORE', [])
# Define default keys to ignore plus user defined ones.
UNUSED_IGNORE = [
    'block',                   # May not call block.super in template when overridding the base.
    'csrf_token',              # Provided to all templates.
    'DEFAULT_MESSAGE_LEVELS',  # Provided to all templates using messages framework.
    'False',                   # Provided to all templates.
    'is_paginated',            # Included by ListView and may not need pagination.
    'None',                    # Provided to all templates.
    'page_obj',                # Included by ListView and may not need pagination.
    'paginator',               # Included by ListView and may not need pagination.
    'perms',                   # Provided to login_required templates.
    'root_urlconf',            # Provided to exception pages for 404.
    'settings',                # Likely to be provided to templates and not used.
    'site',                    # Provided to the login page and may not be used.
    'site_name',               # Provided to the login page and may not be used.
    'True',                    # Provided to all templates.
    'view',                    # Provided to built-in password reset page.
] + django_unused_context_ignore

# Set up lock.
lock = threading.Lock()


@contextlib.contextmanager
def warn_unused_context(request):
    """
    Warn if unused keys in context when using request.
    Currently ignores admin pages.
    """
    if request.path.startswith('/admin/'):
        yield  # Let caller get the response.
        return  # Ignore admin pages.

    # NOTE: Monkeypatching is not threadsafe.
    lock.acquire()

    # Save original functionality for restoration after monkeypatching.
    __orig_getitem__ = Context.__getitem__

    # Create a set for both used keys and all keys. Init used to the ones to ignore.
    used_keys = set(UNUSED_IGNORE)
    all_keys = set()

    def __getitem__(self, lookup_key):
        # If all keys not set, set it and ignore exceptions.
        if not all_keys:
            # Initialize default dict for flattening all context vars on error.
            flattened = {}

            try:
                # Try to flatten all context vars.
                flattened = self.flatten()
            except Exception as err:
                # Exceptions here are usually caused because a template tag
                # returned a Context() object instead of a plain dictionary.
                logger.exception(f"Ignoring context error: {err}")
                raise
            # Create all_keys dictionary.
            for key, value in flattened.items():
                if value:
                    # Add to all keys
                    all_keys.add(key)

        # Add the key that was used to get a context item to the used_keys set.
        used_keys.add(lookup_key)
        # Return the default behavior by using the original getitem function.
        return __orig_getitem__(self, lookup_key)

    try:
        # Monkeypatch context to keep track of unused variables in context.
        Context.__getitem__ = __getitem__

        # Let caller get the response.
        yield
    finally:
        # Un-patch it.
        Context.__getitem__ = __orig_getitem__
        # Un-patching complete so release the lock.
        lock.release()

    # Check for unused keys.
    unused = all_keys.difference(used_keys)

    # If there are unused keys add warning and log message pointing them out.
    if unused:
        msg = f"Request Context {request} had unused keys: {unused}"
        warnings.warn(msg)
        logger.warning(msg)


class UnusedContextMiddleware:
    """
    Unused Context Middleware
    Logs warnings if keys in context are not used in template.
    """
    def __init__(self, get_response):
        """
        Save the get_response method for later use.
        """
        self.get_response = get_response


    def __call__(self, request):
        """
        Return standard response using warn_unused_context
        """
        with warn_unused_context(request):
            response = self.get_response(request)
            return response
