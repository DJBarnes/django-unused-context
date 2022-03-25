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
    'None',
    'False',
    'True',
] + django_unused_context_ignore

# Set up lock.
lock = threading.Lock()


@contextlib.contextmanager
def warn_unused_context(request):
    """Warn if unused keys in context when using request.
    Currently ignores admin pages
    Usage:
        with warn_unused_context(request):
            response = self.get_response(request)

    This will monkeypatch Context's __getitem__ method to keep track of unused
    keys in the context.
    """
    if request.path.startswith('/admin/'):
        yield  # Let caller get the response.
        return  # Ignore admin pages.

    # NOTE: Monkeypatching is not threadsafe.
    lock.acquire()

    # Monkeypatch context to keep track of unused keys in context.
    __orig_getitem__ = Context.__getitem__

    used_keys = set(UNUSED_IGNORE)
    all_keys = set()

    def __getitem__(self, get_item_key):
        # If all_keys does not exist, create it.
        if not all_keys:
            # Create default flattened dict.
            flattened = {}

            try:
                # Take the data in this context and flatten it to a flattened dict.
                flattened = self.flatten()
            except Exception as err:
                # Exceptions here are usually caused because a template tag
                # returned a Context() object instead of a plain dictionary.
                logger.exception("Ignoring context error: %s", err)
                raise
            # For each key, value in the flattened context dict.
            for key, val in flattened.items():
                if val:
                    # Add to all_keys.
                    all_keys.add(key)

        # Add get_item_key to the set of used keys.
        used_keys.add(get_item_key)
        # Return the default functionality of __getitem__.
        return __orig_getitem__(self, get_item_key)

    try:
        # Try to monkey patch the __getitem__ function of Context.
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

    # If there are unused keys, add warnings and log warnings about the unused keys.
    if unused:
        msg = "Request Context %s had unused keys: %s"
        warnings.warn(msg % (request, unused))
        logger.warning(msg, request, unused)

class UnusedContextMiddleware:
    """
    UnusedContext Middleware.
    Logs warnings if keys in context are not used in template.
    """
    def __init__(self, get_response):
        """
        Save get_response function to class for later use.
        """
        self.get_response = get_response


    def __call__(self, request):
        """
        Return standard response using warn_unused_context.
        """
        with warn_unused_context(request):
            return self.get_response(request)
