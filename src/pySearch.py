"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015
    @Purpose:       The purpose of this algorithm is to accept a search string along with a search engine type.
                    Search engine types may include:
                        Bing
                        Google
                        Yahoo
                    The program will then search the engine type using one of the libraries available for the search engine and 
                    retrieve a data set of results. This data set of results will then be categorized by system attribute. The system 
                    attributes sought will be as follows:
                        
"""

import sys
import argparse
from pyBing import *
from pyGoogle import *
from pyYahoo import *
import os
import time

print("Starting Search ......")

# --------------------------------------------------------------------------
# Global Configuration
# --------------------------------------------------------------------------
_MODE = "DEBUG"
_source = os.getcwd()+'\\inputs\\californiaCities.txt'
# --------------------------------------------------------------------------

parser = argparse.ArgumentParser(prog='pySearch.py')
parser.add_argument('-engine', help='Search Engine [BING | GOOGLE | YAHOO]')

parse = parser.parse_args()

if parse.engine:
    if _MODE == "DEBUG":
        print("Engine: %s" % parse.engine)
    
    if not os.path.exists(os.getcwd()+'\\'+parse.engine.upper()):
        os.makedirs(os.getcwd()+'\\'+parse.engine.upper())
    
    _file = open(_source, 'r')
    _term = _file.readline().strip()
    while _term:
        print("Searching: %s" % _term)
        
        if parse.engine.upper() == 'BING':
            _bing = pyBing(_term)
        elif parse.engine.upper() == 'GOOGLE':
            _google = pyGoogle(_term)
        elif parse.engine.upper() == 'YAHOO':
            _yahoo = pyYahoo(_term)
            
        _term = _file.readline().strip()
        
    _file.close()
    
else:
    parser.print_help()

print("Ending Search ......")