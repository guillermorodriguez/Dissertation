"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015
    @Purpose:       The purpose of this algorithm is to accept a search string along with a search engine type.
                    Search engine types may include:
                        Bing
                        Google
                        Yahoo
                    The program will then search the engine type using one of the specific URL for the search engine and 
                    retrieve a data set of results. This data set of results will then be categorized by system attribute. The system 
                    attributes sought will be as follows:
                        description
                        div
                        h1
                        h2
                        h3
                        h4
                        h5
                        h6
                        inbound_links
                        keywords
                        outbound_links
                        p
                        root
                        span
                        title
                    The keyword that will be used to search the data set will be chosen at random from a series of alphabet words that are 
                    contained in the file called words.txt
"""

import sys
import argparse
from pyBing import *
from pyGoogle import *
from pyYahoo import *
import os
import time
import random

print("Starting Search ......")

parser = argparse.ArgumentParser(prog='pySearch.py')
parser.add_argument('-engine', help='Search Engine [BING | GOOGLE | YAHOO]')
parse = parser.parse_args()

# --------------------------------------------------------------------------
# Global Configuration
# --------------------------------------------------------------------------
_MODE = "DEBUG"
_source = os.getcwd()+'\\words_chosen.txt'
_use_proxy = False
_words = []

# Ensure Default Search Engine Directory Exists
if not os.path.exists(os.getcwd()+'\\'+parse.engine.upper()):
    os.makedirs(os.getcwd()+'\\'+parse.engine.upper())
# --------------------------------------------------------------------------

if parse.engine:
    if _MODE == "DEBUG":
        print("Engine: %s" % parse.engine)
    
    with open(_source, 'r') as _file:
        for _line in _file:
            _term = _line.strip()
            if _term[0:1] != "#":
                print("Searching: %s" % _term)  

                if parse.engine.upper() == 'BING':
                    _bing = pyBing()
                    _bing.getLinks(_term)
                elif parse.engine.upper() == 'GOOGLE':            
                    _google = pyGoogle()
                    _google.getLinks(_term, _use_proxy)           
                    time.sleep(10)
                elif parse.engine.upper() == 'YAHOO':
                    _yahoo = pyYahoo()            
                    _yahoo.getLinks(_term)
else:
    parser.print_help()

print("Ending Search ......")