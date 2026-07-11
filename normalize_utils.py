import os
import json
import time
import shutil

import re
import unicodedata

from lib import g
from lib import io

def normalize_plant_name(name):
    # Common botanical author abbreviations (extend over time)
    AUTHOR_PATTERNS = [
        r"\bL\.\b",
        r"\bLinn\.\b",
        r"\bDC\.\b",
        r"\bHook\.?\s*f?\.?\b",
        r"\bBenth\.\b",
        r"\bWilld\.\b",
        r"\bMill\.\b",
        r"\bLam\.\b",
        r"\bRoxb\.\b",
    ]
    AUTHOR_REGEX = re.compile("|".join(AUTHOR_PATTERNS), re.IGNORECASE)
    if not name:
        return ""
    # Unicode normalization
    name = unicodedata.normalize("NFKC", name)
    # lowercase
    name = name.lower()
    # normalize hybrid sign
    name = name.replace("×", " x ")
    # remove botanical author citations
    name = AUTHOR_REGEX.sub("", name)
    # remove punctuation except letters, numbers and spaces
    name = re.sub(r"[.,;:()\[\]{}]", " ", name)
    # collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()
    return name

def normalize_chemical_name(name):
    spaces = re.compile(r"\s+")
    name = unicodedata.normalize("NFKC", name)
    name = name.lower()
    name = name.replace("-", " ")
    name = spaces.sub(" ", name)
    return name.strip()

def normalize_activity_name(name):
    spaces = re.compile(r"\s+")
    if not name: return None
    name = unicodedata.normalize("NFKC", name)
    name = name.lower()
    name = name.replace("-", " ")
    name = re.sub(r"[.,;:]", "", name)
    name = spaces.sub(" ", name)
    return name.strip()
