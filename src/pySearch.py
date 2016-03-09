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

print("Starting Search ......")

# --------------------------------------------------------------------------
# Global Configuration
# --------------------------------------------------------------------------
_MODE = "DEBUG"
# --------------------------------------------------------------------------

parser = argparse.ArgumentParser(prog='pySearch.py')
parser.add_argument('-engine', help='Search Engine [BING | GOOGLE | YAHOO]')
parser.add_argument('-search', help='Search Term')
parser.add_argument('-results', help='Search Results')
parser.add_argument('-api', help='Use API [True | False]')
parse = parser.parse_args()

if parse.engine and parse.search and parse.results and parse.api:
    if _MODE == "DEBUG":
        print("Engine: %s" % parse.engine)
        print("Search: %s" % parse.search)
        print("Results: %s" % parse.results)
        print("API: %s" % parse.api)
        
    if parse.engine.upper() == 'BING':
        _bing = pyBing(parse.search, parse.results, parse.api)
    elif parse.engine.upper() == 'GOOGLE':
        _google = pyGoogle(parse.search, parse.results, parse.api)
    elif parse.engine.upper() == 'YAHOO':
        _yahoo = pyYahoo(parse.search, parse.results, parse.api)
else:
    parser.print_help()

print("Ending Search ......")