"""Test Views"""
import warnings
from django.test import TestCase
from django.test import override_settings


@override_settings(DEBUG=True)
class DumpDieViewSimpleTestCase(TestCase):
    """Class for testing unused context from a view"""

    def test_using_all_context_vars_does_not_raise_warnings(self):
        """Test that using all context vars does not raise any warnings"""
        with warnings.catch_warnings(record=True) as test_warnings:
            self.client.get("/all_context")

            self.assertEqual(len(test_warnings), 0)

    def test_using_some_context_vars_raises_warnings_about_unused_context(self):
        """Test that using some context vars does raise some warnings"""
        warning_message = (
            "Request Context <WSGIRequest: GET '/some_context'> had unused keys:"
        )
        warning_number = "number"

        with warnings.catch_warnings(record=True) as test_warnings:
            self.client.get("/some_context")

            self.assertEqual(len(test_warnings), 1)
            self.assertIn(warning_message, str(test_warnings[-1].message))
            self.assertIn(warning_number, str(test_warnings[-1].message))

    def test_using_no_context_vars_raises_warnings_about_unused_context(self):
        """Test that using no context vars does raise warnings"""
        warning_message = (
            "Request Context <WSGIRequest: GET '/no_context'> had unused keys:"
        )
        warning_name = "name"
        warning_number = "number"

        with warnings.catch_warnings(record=True) as test_warnings:
            self.client.get("/no_context")

            self.assertEqual(len(test_warnings), 1)
            self.assertIn(warning_message, str(test_warnings[-1].message))
            self.assertIn(warning_name, str(test_warnings[-1].message))
            self.assertIn(warning_number, str(test_warnings[-1].message))

    override_settings(DJANGO_UNUSED_CONTEXT_IGNORE=["number"])

    def test_using_no_context_vars_ignores_ones_set_by_ignore_setting_when_raising_warnings(
        self,
    ):
        """Test that using no context vars ignores ones set by ignore setting when raising warnings"""
        warning_message = (
            "Request Context <WSGIRequest: GET '/no_context'> had unused keys:"
        )
        warning_name = "name"

        with warnings.catch_warnings(record=True) as test_warnings:
            self.client.get("/no_context")

            self.assertEqual(len(test_warnings), 1)
            self.assertIn(warning_message, str(test_warnings[-1].message))
            self.assertIn(warning_name, str(test_warnings[-1].message))

    @override_settings(DEBUG=False)
    def test_using_no_context_vars_does_not_raise_warnings_about_unused_context_when_debug_is_false(
        self,
    ):
        """Test that using no context vars does not raise warnings about unused context when debug is false"""

        with warnings.catch_warnings(record=True) as test_warnings:
            self.client.get("/no_context")

            self.assertEqual(len(test_warnings), 0)

    @override_settings(DEBUG=False, DJANGO_UNUSED_CONTEXT_ALWAYS=True)
    def test_using_no_context_vars_raises_warnings_about_unused_context_when_debug_is_false_but_alway_is_true(
        self,
    ):
        """Test that using no context vars does raise warnings"""
        warning_message = (
            "Request Context <WSGIRequest: GET '/no_context'> had unused keys:"
        )
        warning_name = "name"
        warning_number = "number"

        with warnings.catch_warnings(record=True) as test_warnings:
            self.client.get("/no_context")

            self.assertEqual(len(test_warnings), 1)
            self.assertIn(warning_message, str(test_warnings[-1].message))
            self.assertIn(warning_name, str(test_warnings[-1].message))
            self.assertIn(warning_number, str(test_warnings[-1].message))
