# -*- coding: utf-8 -*-
"""Setup script for CS111-Green-Utilities"""

import setuptools

from cs_green_utils import __version__ as cgu_version
from cs_green_utils import __author__ as cgu_author
from cs_green_utils import __author_email__ as cgu_author_email
from cs_green_utils import __description__ as cgu_description

with open('requirements.txt', 'r') as f:
    reqs = f.read()

reqs = reqs.split('\n')[0:-1]

setuptools.setup(
    name='cs_green_utils',
    version=cgu_version,
    author=cgu_author,
    author_email=cgu_author_email,
    description=cgu_description,
    long_description=cgu_description,
    long_description_content_type='text/plain',
    url='https://github.com/karolisr/CS111-Green-Utilities',
    packages=setuptools.find_packages(),
    install_requires=reqs,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: cc-by-sa-4.0',
        'Operating System :: OS Independent',
    ]
)
