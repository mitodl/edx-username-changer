"""
Django admin pages for edx-username-changer plugin
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model

# pylint: disable=import-error
from common.djangoapps.student.admin import (
    UserAdmin as BaseUserAdmin,
)


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    """
    Admin interface for the User model.
    """

    def get_readonly_fields(self, request, obj=None):
        """
        It will remove 'username' from the read-only fields to make it editable through the admin panel
        """
        readonly_fields = super().get_readonly_fields(request, obj)
        if settings.FEATURES.get("ENABLE_EDX_USERNAME_CHANGER") and obj:
            # pylint: disable=consider-using-generator
            return tuple([name for name in readonly_fields if name != "username"])
        return readonly_fields


# We must first un-register the User model since it was registered by edX's core code.
try:
    # pylint: disable=undefined-variable
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, UserAdmin)
