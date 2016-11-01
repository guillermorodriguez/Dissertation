import os
import argparse

print ('Started ....')
# --------------------------------------------------------------------------
# Global Configuration
# --------------------------------------------------------------------------
_MODE = "DEBUG"
# --------------------------------------------------------------------------

parser = argparse.ArgumentParser(prog='merge.py')
parser.add_argument('-engine', help='Search Engine [BING | GOOGLE | YAHOO]')
parse = parser.parse_args()

if parse.engine:
    
    path = os.getcwd()+'\\'+parse.engine
    type = '.data'
    destination = path + '\\_compiled.dat'
    
    if os.path.exists(destination):
        os.remove(destination)
        
    for _file in os.listdir(path):
        if type in _file:
            with open(path+'\\'+_file) as _source:
                if not os.path.exists(destination):
                    with open(destination, 'w') as _target:
                        for _line in _source:
                            _target.write(_line)
                else:
                    with open(destination, 'a') as _target:
                        for _line in _source:
                            if 'index' in _line:
                                continue
                            else:
                                _target.write(_line)
else:
    parser.print_help()
    
print ('Ended ....')