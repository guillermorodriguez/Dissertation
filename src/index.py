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
parser.add_argument('-operation', help='Operation [index | consolidate]')
parse = parser.parse_args()

if parse.engine and parse.operation:    
    if parse.operation.lower() == 'index':
        _path = os.getcwd()+'\\'+parse.engine+'\\data\\'
        _type = '.data'
        _destination = '_indexed.dat'

        if os.path.exists(_path+_destination):
            os.remove(_path+_destination)

        with open(_path+_destination, 'w') as _target:
            _target.write('index\tkey\turl\tdescription\tdiv\th1\th2\th3\th4\th5\th6\tinbound_links\tkeywords\toutbound_links\tp\troot\tspan\ttitle\n')

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
                                    _target.write(_data[0]+'\t'+_name_pairs[0]+'\t'+_data[1])
                                    for _index in _indexes:
                                        _target.write('\t'+str(_index[1]))
                                    _target.write('\n')    
                                    
    elif parse.operation.lower() == 'consolidate':
        # Determines the average index for each node found
        print("Consolidating....")
        _path = os.getcwd()+'\\'+parse.engine+'\\data\\'
        _source = '_indexed.dat'
        _destination = '_clean.dat'
        
        # Get Distinct URLs
        _sites = []
        with open(_path+_source, 'r') as _from:
            for _line in _from:
                _data = _line.split('\t')
                if _data[0] != 'index':
                    if len(_sites) == 0:
                        _sites.append({'index': _data[0], 'key': _data[1] , 'url': _data[2], 'indexes': _data[3:]})
                    _exists = False
                    for _site in _sites:
                        if _data[1] == _site['key'] and _site['url'] == _data[2]:
                            _exists = True
                            break
                    if not _exists:
                        _sites.append({'index': _data[0], 'key': _data[1] , 'url': _data[2], 'indexes': _data[3:]})
                        print("Added: %s" % _data[2])
        
        # Get Average Index
        _cleaned = []
        for _site in _sites:
            _compositeIndex = float(_site['index'])
            _count = 1.0
            with open(_path+_source, 'r') as _from:
                for _line in _from:
                    _data = _line.split('\t')
                    if _data[0] != 'index' and _data[1] == _site['key'] and _data[2] == _site['url']:
                        _count+=1 
                        _compositeIndex+=float(_data[0])
                        
            _cleaned.append({'index': _compositeIndex/_count, 'key': _site['key'] , 'url': _site['url'], 'indexes': _site['indexes']})
        
        if os.path.exists(_path+_destination):
            os.remove(_path+_destination)
            
        with open(_path+_destination, 'w') as _target:
            _target.write('index\tkey\turl\tdescription\tdiv\th1\th2\th3\th4\th5\th6\tinbound_links\tkeywords\toutbound_links\tp\troot\tspan\ttitle\n')
       
        for _clean in _cleaned:
            with open(_path+_destination, 'a') as _file:
                _file.write(str(_clean['index']) + '\t' + _clean['key'] + '\t' + _clean['url'])
                for _entry in _clean['indexes']:
                    _file.write('\t'+ str(_entry).strip())
                _file.write('\n')
            
            
else:
    parser.print_help()
    
print ('Ended ....')