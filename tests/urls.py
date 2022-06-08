"""
django_unused_context URL Configuration.
Used exclusively to test package.
"""

from django.urls import path

from . import views


urlpatterns = [
    path("all_context", views.all_context, name="all_context"),
    path("some_context", views.some_context, name="some_context"),
    path("no_context", views.no_context, name="no_context"),
]
