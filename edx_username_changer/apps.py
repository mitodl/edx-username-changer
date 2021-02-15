"""
App configuration for edx-username-changer plugin
"""

from django.apps import AppConfig


class EdxUsernameChangerConfig(AppConfig):
    name = 'edx_username_changer'
    verbose_name = "Open edX Username Changer"

    def ready(self):
        """
        Connect signal handlers.
        """
        from . import signals  # pylint: disable=unused-import
