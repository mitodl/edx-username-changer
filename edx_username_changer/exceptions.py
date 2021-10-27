"""
Exceptions for edx-username-changer plugin
"""


# pylint: disable=super-init-not-called
class UpdateFailedException(Exception):
    """
    Exception to throw when there is an update failure in username
    """

    def __init__(self, url, new_username):
        self.url = url
        self.new_username = new_username

    def __str__(self):
        return (
            f"Username update failed for username: {self.new_username}, url: {self.url}"
        )
