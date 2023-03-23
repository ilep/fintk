# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:15:32 2020

@author: ilepoutre
"""

# https://pypi.org/project/python-dotenv/

# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1

import os
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = Path(os.path.dirname(os.path.realpath(__file__))) / '.env'
load_dotenv(dotenv_path=dotenv_path)

DATA = Path(os.getenv('DATA'))
EOD_API_KEY = os.getenv('EOD_API_KEY') 


