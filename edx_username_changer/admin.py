"""
Django admin pages for edx-username-changer plugin
"""

from django.contrib import admin
from django.contrib.auth import get_user_model

from common.djangoapps.student.admin import UserAdmin as BaseUserAdmin


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    """
    Admin interface for the User model.
    """

    def get_readonly_fields(self, request, obj=None):
        """
        It will remove 'username' from readonly field to make it editable through admin panel
        """
        readonly_fields = super(UserAdmin, self).get_readonly_fields(request, obj)
        if obj:
            return tuple([name for name in readonly_fields if name != "username"])
        return readonly_fields


# We must first un-register the User model since it was registered by edX's core code.
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, UserAdmin)