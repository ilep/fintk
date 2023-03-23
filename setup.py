# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:54:15 2022

@author: ilepoutre
"""

# pip install -e . (depuis le dossier)

from setuptools import setup

setup(name='fintk',
version='0.0.1',
description='Financial python lib for asset management using eodhistoricaldata among others',
url='https://github.com/ilep/fintk.git',
author='Ivan Lepoutre',
author_email='ivanlptr@gmail.fr',
package_dir={'fintk':'fintk'},
packages=['fintk'],
include_package_data=True,
package_data={'fintk': ['data/*.csv']},
zip_safe=False)

