"""
Execeptions for edx-username-changer plugin
"""


class UpdateFailedException(Exception):
    def __init__(self, url, new_username):
        self.url = url
        self.new_username = new_username

    def __str__(self):
        return "Username update failed for username: {}, url: {})".format(
            self.new_username,
            self.url,
        )
