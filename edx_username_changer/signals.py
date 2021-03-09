"""
Signals and Signal Handlers for edx-username-changer plugin
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver

from common.djangoapps.util.model_utils import get_changed_fields_dict

from edx_username_changer.utils import update_user_social_auth_uid
from edx_username_changer.tasks import task_update_username_in_forum


def user_pre_save_callback(sender, **kwargs):
    """
    Pre-save signal handler of User model to store changed fields to be used later
    """
    if settings.FEATURES.get("ENABLE_EDX_USERNAME_CHANGER"):
        user = kwargs["instance"]
        fields_to_update = get_changed_fields_dict(user, sender)
        if "username" in fields_to_update:
            fields_to_update.update({"new_username": user.username})
            user._updated_fields = fields_to_update


def user_post_save_callback(sender, **kwargs):
    """
    Post-save signal handler of User model to update username throughout the application
    """
    if settings.FEATURES.get("ENABLE_EDX_USERNAME_CHANGER"):
        user = kwargs["instance"]
        if (
            hasattr(user, "_updated_fields")
            and user._updated_fields
            and {"username", "new_username"}.issubset(user._updated_fields)
        ):
            task_update_username_in_forum.delay(user._updated_fields["new_username"])
            update_user_social_auth_uid(user._updated_fields["username"], user._updated_fields["new_username"])

            delattr(user, "_updated_fields")
