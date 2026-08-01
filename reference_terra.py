import os
import time

import sqlite3
import csv
import re
import unicodedata
import time

from lib import g
from lib import io

import normalize_utils

def reference_plant_part():
    pass

def run():
    print(f'REFERENCE >> terra')

    start = time.perf_counter()
    reference_plant_part()
    print(f'drduke table_activities_create() - execution time: ', time.perf_counter() - start)

