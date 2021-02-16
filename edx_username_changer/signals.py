"""
Signals and Signal Handlers for edx-username-changer plugin
"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from common.djangoapps.util.model_utils import get_changed_fields_dict

from edx_username_changer.utils import EdxUsernameChanger


@receiver(pre_save, sender=User)
def user_pre_save_callback(sender, **kwargs):
    """
    Pre-save signal handler of User model to store changed fields to be used later
    """
    user = kwargs['instance']
    fields_to_update = get_changed_fields_dict(user, sender)
    if 'username' in fields_to_update:
        fields_to_update.update({'new_username': user.username})
        user._updated_fields = fields_to_update


@receiver(post_save, sender=User)
def user_post_save_callback(sender, **kwargs):
    """
    Post-save signal handler of User model to update usernames throughout application
    """
    user = kwargs['instance']
    if hasattr(user, '_updated_fields') and user._updated_fields and {'username', 'new_username'}.issubset(user._updated_fields):
        username_changer = EdxUsernameChanger(user._updated_fields['username'], user._updated_fields['new_username'])
        username_changer.update_user_social_auth_uid()
        username_changer.update_username_in_forum()
        delattr(user, '_updated_fields')