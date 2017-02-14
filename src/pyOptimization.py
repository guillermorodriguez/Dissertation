import os
import argparse
from xml.dom import minidom
from htmlHelper import *
from extract import *
from nltk.corpus import wordnet 

print ('Started ....')
# --------------------------------------------------------------------------
# Global Configuration
# --------------------------------------------------------------------------
_MODE = "DEBUG"
# --------------------------------------------------------------------------

parser = argparse.ArgumentParser(prog='pyOptimization.py')
parser.add_argument('-engine', help='Search Engine [BING | GOOGLE | YAHOO]')
parser.add_argument('-operation', help='Optimization Type [INDEX | FILTER]')
parse = parser.parse_args()

nodes = []
if parse.engine and parse.operation:    
        
    if parse.operation and parse.operation.upper() == 'INDEX':
        _path = os.getcwd()+'\\'+parse.engine+'\\data\\'
        _source = '_historical.dat'
    
        _destination = '_historical_indexed.dat'    
        if os.path.exists(_path+_destination):
            os.remove(_path+_destination)    

        with open(_path+_source, 'r') as _process:
            for _line in _process:
                if 'key' in _line and 'sink' in _line and 'source' in _line:
                    with open(_path+_destination, 'w') as _file:
                        _file.write('key\tsink\tsource\tdescription\tdiv\th1\th2\th3\th4\th5\th6\tinbound_links\tkeywords\toutbound_links\tp\troot\tspan\ttitle\n')
                else:
                    _data = _line.strip().split('\t')                
                    if ( len(_data) == 3 ) and  ( len(_data[2].strip()) > 0 ) and ('Unicode Error' not in _data[2].strip()):
                        try:
                            print("Searching: %s" % _data[2])
                            _keywords = []
                            for _synonyms in wordnet.synsets(_data[0]):
                                for _s in _synonyms.lemmas():
                                    _s = _s.name().replace('_', ' ')
                                    if _s not in _keywords:
                                        _keywords.append(_s)
                            if len(_keywords) == 0:
                                _keywords.append(_data[0])
                            print(_keywords)

                            _indexes = sorted(Extract().extract_indexes(_data[2], _keywords ).items())
                            if _indexes:
                                with open(_path+_destination, 'a') as _file:
                                    _file.write(_data[0]+'\t'+_data[1]+'\t'+_data[2])
                                    for _index in _indexes:
                                        _file.write('\t'+str(_index[1]))
                                    _file.write('\n')    
                        except:
                            print("Error Processing URL")
    elif parse.operation and parse.operation.upper() == 'FILTER':
        _path = os.getcwd()+'\\'+parse.engine+'\\data\\'
        _source = '_historical_indexed.dat'
    
        _destination = '_historical_filtered.dat'    
        if os.path.exists(_path+_destination):
            os.remove(_path+_destination)    
        
        with open(_path+_destination, 'w') as _file:
            _file.write('key\tsink\tdescription\tdiv\th1\th2\th3\th4\th5\th6\tinbound_links\tkeywords\toutbound_links\tp\troot\tspan\ttitle\n')
                     
        # Distinct URLs
        _summary = []
        with open(_path+_source, 'r') as _process:
            for _line in _process:
                if ('key' not in _line) and ('sink' not in _line) and ('source' not in _line):
                    _data = _line.strip().split('\t') 
                    
                    _found = False
                    _totals = []
                    for _entry in _summary:
                        if ('url' in _entry)and ( _data[1].strip().lower() in _entry.get('url').strip().lower()):
                            _found = True
                            break
                    if not _found:
                        print("ADDING: %s" %  _data[1])
                        _summary.append({'url': _data[1], 'data': _totals})
        
else:
    parser.print_help()
    
print ('Ended ....')
    

