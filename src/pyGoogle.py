"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015
    @Requires:      Google Search API:
                        
                    http://stackoverflow.com/questions/1657570/google-search-from-a-python-app
    @Purpose:                               
"""
import sys
from config import *
import json
import urllib.request
import traceback
from htmlHelper import *
from extract import *
import time
import os
from nltk.corpus import wordnet 

class pyGoogle(Extract):
    """ 
        
    """
    
    _proxy = False
    
    def __init__(self):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')
        
    def getBackLinks(self, url):
        _repository = {}
        _page = 1
        _iteration = "&start=[ITERATION_STEP]"
        _MAX = 100
        try:
            
        except request.URLError as e:
            print("Error: %s" % e.reason )
        except ValueError as v:
            print("Non urllib Error: %s" % v)
            
        return _repository

    # Extract Link Attributes for a Given Search
    def getLinks(self, query, use_proxy = False):
        # Obtain API Settings
        _config = config()
        _config.google()
        
        self._proxy = use_proxy
        try:
            # Keywords
            _keywords = []
            for _synonyms in wordnet.synsets(query):
                for _s in _synonyms.lemmas():
                    _s = _s.name().replace('_', ' ')
                    if _s not in _keywords:
                        _keywords.append(_s)
            if len(_keywords) == 0:
                _keywords.append(query)
            
            # Set Repository Structure
            _name = os.getcwd()+'\\GOOGLE\\'+query+'_'+time.strftime("%Y%m%d%H%M%S")+".data"
            _file = open( _name, "w" )   
            _file.write('index\turl\tdescription\tdiv\th1\th2\th3\th4\th5\th6\tinbound_links\tkeywords\toutbound_links\tp\troot\tspan\ttitle\n')
            _file.close()
            # Direct Call                  
            _html = self.extract_links(_config.google_settings['url']+query, 'GOOGLE', use_proxy)
            _indexValue = 0
            _page = 1
            _maxPages = 11
            while _html.next != '' and _page < _maxPages:
                for _entry in _html.links:
                    _indexValue += 1
                    if '.pdf' not in _entry:
                        print("Searching: %s" % _entry['url'])
                        _indexes = sorted(self.extract_indexes(_entry['url'], _keywords).items())
                        if _indexes:
                            _file = open(_name, 'a')
                            _file.write(str(_indexValue) + '\t' + _entry['url'] )
                            for _index in _indexes:
                                _file.write('\t'+str(_index[1]))
                            _file.write('\n')    
                            _file.close()
                    
                if _html.next != '':
                    print("Next: %s" % _html.next)
                    _html = self.extract_links(_html.next, 'GOOGLE') 
                    print("Pausing for 3 seconds")
                    time.sleep(3)
                    
                    _page += 1
                    
        except urllib.request.URLError as e:
            print("URL Error: %s" % e.reason )
            self._proxy = True
            self.getLinks(query, True)
        except ValueError as v:
            print("Value Error: %s" % v)

        