
import sys
import os
import random

print("Started ....")

_source = os.getcwd()+'\\words.txt'
_words = []

_archive = os.getcwd()+'\\words_chosen.txt'
if not os.path.isfile(_archive):
    # Create Query History File
    _queries = open(_archive, 'w')
    _queries.close()

# Read Dictionary
with open(_source, 'r') as _file:
    for _line in _file:
        if len(_line.strip()) > 1:
            _words.append(_line.strip())
    _file.close()

# Select 100 Random Words
for iteration in range(100):
    _term = random.choice(_words)
    with open(_archive, 'a') as _file:
        _file.write(_term)
        _file.write('\n')
        _file.close()

print("Completed ....")