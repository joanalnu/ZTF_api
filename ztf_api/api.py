# importing libraries
import subprocess
import os
from astropy.coordinates import Angle
from astropy import units as u
from astropy.time import Time
import requests
import math
import re
dirpath = os.path.dirname(os.path.abspath(__file__))[:-8]

def get_credentials():
    with open(dirpath+'/credentials.txt', 'r') as f