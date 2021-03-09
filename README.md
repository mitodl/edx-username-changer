# edx-username-changer
A plugin to enable update usernames through admin panel in Open edX (and other apps that log into Open edX via OAuth). It only supports koa and latest releases of Open edX.

## Installation

# Installing Plugin
You can install it into any Open edX instance by using the following two methods:

To get the latest stable release from PyPI

```bash
pip install edx-username-changer
```

To get the latest commit from GitHub

```bash
pip install -e git+https://github.com/mitodl/edx-username-changer.git@master#egg=edx-username-changer
```
# Configuring Plugin into Open edX
To configure this plugin, you need to do the following one step:

1) Add/Enable a feature flag (ENABLE_EDX_USERNAME_CHANGER) into your environment variables (through lms.yml or studio.yml, depending upon where you are installing the plugin)
```bash
FEATURES:
  ...
  ...
  ENABLE_EDX_USERNAME_CHANGER: true
  ...
```

## How To Use
Its usage is as simple as changing the username of a user account through django's admin panel.
Here are the steps (for clarity):

1) Install `edx-username-changer` plugin.
2) Use an admin account to `access django admin` panel.
3) Go to `Users` model and `select an account` to change its username.
4) In the account editor page change the `username` field.
5) Hit `Save` (present at the bottom-right of page).

The whole process can be done on `lms` or `studio` or on both of them.
