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
                    for _entry in _summary:
                        if (_data[1].strip().lower() == _entry.strip().lower()):
                            _found = True
                            break
                    if not _found:
                        print("ADDING: %s" %  _data[1])
                        _summary.append( _data[1])
        
        for _individual in _summary:
            _totals = []
            _found = 0
            with open(_path+_source, 'r') as _process:
                for _line in _process:
                    if ('key' not in _line) and ('sink' not in _line) and ('source' not in _line):
                        _data = _line.strip().split('\t') 
                        if _individual.strip().lower() == _data[1].strip().lower():                            
                            _index = 3
                            while _index < len(_data[3:]):
                                if _found == 0:
                                    if _data[_index].isnumeric():
                                        try:
                                            _totals.append(float(_data[_index])) 
                                        except:
                                            _totals.append(float(0))
                                    else:
                                        _totals.append(float(0)) 
                                else:
                                    if _data[_index].isnumeric():
                                        try:
                                            _totals[_index-3] += float(_data[_index])
                                        except:
                                            pass
                                    else:
                                        _totals[_index-3] += 0
                                _index+=1
                            _found+=1
                        else:
                            if _found > 0: 
                                break
            _total = 0
            print(_totals)
            for _entry in _totals:
                _total += _entry
            _total = _total / _found
            with open(_path+_destination, 'a') as _file:
                print("Totals %s = %s" % (_individual, str(_total)))
                _file.write(_individual+'\t'+str(_total)+'\n')
            
else:   
    parser.print_help()
    
print ('Ended ....')
    

