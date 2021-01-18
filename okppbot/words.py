import os
import re


def sanitize(s):
    return re.sub(r'[^a-z0-9\s]', '', s.lower())


WORDS = {sanitize(l) for l in open(os.path.join(os.path.dirname(__file__), 'words.txt'))}
