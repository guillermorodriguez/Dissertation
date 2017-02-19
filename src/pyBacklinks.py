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
_OPERATION = 'APPEND'
# --------------------------------------------------------------------------

parser = argparse.ArgumentParser(prog='pyBacklinks.py')
parser.add_argument('-engine', help='Search Engine [BING | GOOGLE | YAHOO]')
parse = parser.parse_args()

_out = os.getcwd()+'\\'+parse.engine.upper()+'\\data\\_complete.dat'
if _OPERATION != 'APPEND':
    if os.path.exists(_out):
        os.remove(_out)

_historical = os.getcwd()+'\\'+parse.engine.upper()+'\\data\\_historical.dat'
if _OPERATION != 'APPEND':
    if os.path.exists(_historical):
        os.remove(_historical)    
    with open(_historical, 'w') as _file:
        _file.write('key\tsink\tsource\n')
    
if parse.engine:
    source = os.getcwd()+'\\'+parse.engine.upper()+'\\data\\_clean.dat'    
    with open(source) as _source:
        for _line in _source:
            if 'index' in _line and 'url' in _line and 'description' in _line and 'div' in _line and _OPERATION != 'APPEND':                              
                _file = open( _out, "w" )   
                _file.write(_line)
                _file.close()
            elif _line[0:1] != "#":
                _data = _line.strip().split('\t')
                _repository = {}
                if parse.engine.upper() == 'BING':                    
                    _bing = pyBing()           
                    _repository = _bing.getBackLinks(_data[2])   
                elif parse.engine.upper() == 'GOOGLE':
                    _google = pyGoogle()                    
                    while ( len(_repository) == 0 ) or ( len(_repository) == 1 and _repository[0] == 'ERROR' ):
                        _repository = _google.getBackLinks(_data[2])
                        
                elif parse.engine.upper() == 'YAHOO':
                    _yahoo = pyYahoo()
                    _repository = _yahoo.getBackLinks(_data[2])                
                
                if len(_repository) > 0 and len(_repository[0]) > 0:
                    _data[11] = len(_repository)
                else:
                    _data[11] = 0

                _file = open(_out, 'a')
                _entries = ''
                for _entry in _data:
                    if len(_entries) > 0:
                        _entries += '\t'
                    _entries += str(_entry)
                _file.write(_entries+'\n')
                _file.close()
                
                # Log Total Links to File
                try:
                    for _sink in _repository:
                        with open(_historical, 'a') as _log:
                            _log.write(_data[1] + '\t' + _data[2] + '\t' + _sink + '\n')
                except:
                    for _sink in _repository:
                        with open(_historical, 'a') as _log:
                            _log.write(_data[1] + '\t' + _data[2] + '\t[Unicode Error Write]\n')
                
                time.sleep(5)
else:
    parser.print_help()
    
print ('Ended ....')