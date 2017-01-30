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

parser = argparse.ArgumentParser(prog='index.py')
parser.add_argument('-engine', help='Search Engine [BING | GOOGLE | YAHOO]')
parse = parser.parse_args()

if parse.engine:    
    _path = os.getcwd()+'\\'+parse.engine+'\\data\\'
    _type = '.data'
    _destination = '_indexed.dat'
    
    if os.path.exists(_path+_destination):
        os.remove(_path+_destination)
    
    with open(_path+_destination, 'w') as _target:
        _target.write('index\turl\tdescription\tdiv\th1\th2\th3\th4\th5\th6\tinbound_links\tkeywords\toutbound_links\tp\troot\tspan\ttitle\n')
    
    for _file in os.listdir(_path):
        if _type in _file:
            _name_pairs = _file.split('_')       
            _keywords = []
            for _synonyms in wordnet.synsets(_name_pairs[0]):
                for _s in _synonyms.lemmas():
                    _s = _s.name().replace('_', ' ')
                    if _s not in _keywords:
                        _keywords.append(_s)
            if len(_keywords) == 0:
                _keywords.append(_name_pairs[0])
                        
            with open(_path+_file) as _from:        
                for _line in _from:
                    _data = _line.split('\t')
                    if _data[0] != 'index':
                        print("Indexing: %s" % _data[1])
                        _extract = Extract()
                        _indexes = sorted(_extract.extract_indexes(_data[1], _keywords ).items())
                        if _indexes:                        
                            with open(_path+_destination, 'a') as _target:
                                _target.write(_data[0]+'\t'+_data[1])
                                for _index in _indexes:
                                    _target.write('\t'+str(_index[1]))
                                _target.write('\n')    
else:
    parser.print_help()
    
print ('Ended ....')