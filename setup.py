import os
import setuptools
from edx_username_changer import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name="edx-username-changer",
    version=__version__,
    author="MIT Office of Digital Learning",
    description="An edX plugin to change username of edx accounts through admin panel",
    license="GNU AFFERO GENERAL PUBLIC LICENSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
    ],
    url="https://github.com/mitodl/edx-username-changer.git",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "lms.djangoapp": [
            "edx_username_changer = edx_username_changer.apps:EdxUsernameChangerConfig",
        ],
        "cms.djangoapp": [
            "edx_username_changer = edx_username_changer.apps:EdxUsernameChangerConfig",
        ],
    },
)
