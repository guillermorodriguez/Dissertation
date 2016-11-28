import os
import time
import argparse
from pyBing import *
from pyGoogle import *
from pyYahoo import *

print ('Started ....')
# --------------------------------------------------------------------------
# Global Configuration
# --------------------------------------------------------------------------
_MODE = "DEBUG"
# --------------------------------------------------------------------------

parser = argparse.ArgumentParser(prog='pyBacklinks.py')
parser.add_argument('-engine', help='Search Engine [BING | GOOGLE | YAHOO]')
parse = parser.parse_args()

_out = os.getcwd()+'\\'+parse.engine.upper()+'\\_clean_'+time.strftime("%Y%m%d%H%M%S")+".dat"
if parse.engine:
    source = os.getcwd()+'\\'+parse.engine.upper()+'\\_compiled.dat'    
    with open(source) as _source:
        for _line in _source:
            if 'index' in _line and 'url' in _line and 'description' in _line and 'div' in _line:                              
                _file = open( _out, "w" )   
                _file.write(_line)
                _file.close()
            else:
                _data = _line.strip().split('\t')
                if parse.engine.upper() == 'BING':                    
                    _bing = pyBing()                  
                    _data[10] = _bing.getBackLinks(_data[1])                  
                elif parse.engine.upper() == 'YAHOO':
                    _yahoo = pyYahoo()
                    _data[10] = _yahoo.getBackLinks(_data[1])
                    
                _file = open(_out, 'a')
                _entries = ''
                for _entry in _data:
                    if len(_entries) > 0:
                        _entries += '\t'
                    _entries += str(_entry)
                _file.write(_entries+'\n')
                _file.close()              
                time.sleep(3)
else:
    parser.print_help()
    
print ('Ended ....')