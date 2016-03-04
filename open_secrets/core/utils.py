import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(variable_name):
    """Get the environment variable for the specified name"""
    try:
        return os.environ[variable_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(variable_name)
        raise ImproperlyConfigured(error_msg)
