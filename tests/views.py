"""Views for testing Unused Context"""
from django.shortcuts import render


def all_context(request):
    """Use All Context Example Test View."""
    return render(
        request,
        "all_context.html",
        {
            "name": "example_name",
            "number": 12,
            "site": "example.com",  # Simulating site, an ignored one with string.
        },
    )


def some_context(request):
    """Use Some Context Example Test View."""
    return render(
        request,
        "some_context.html",
        {
            "name": "example_name",
            "number": 12,
            "site": "example.com",  # Simulating site, an ignored one with string.
        },
    )


def no_context(request):
    """Use no Context Example Test View."""
    return render(
        request,
        "no_context.html",
        {
            "name": "example_name",
            "number": 12,
            "site": "example.com",  # Simulating site, an ignored one with string.
        },
    )
