"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015 
    @Purpose:       The purpose of this class is to perform a query through a call to the Bing.com search page. The data set in the response is parsed
                    and evaluated for attribute significance. The algorithm searches the first 'n' pages for a sereies of results.  
"""

import sys
from config import *
import urllib.request as request
from xml.dom import minidom
from htmlHelper import *
from extract import *
import time
import os
import math
from nltk.corpus import wordnet 

class pyBing(Extract):
    
    def __init__(self):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')
        
    def getBackLinks(self, url):
        _repository = {}
        _page = 1
        _iteration = "&first=[ITERATION_STEP]&FORM=PORE"
        try:
            print("Page %i" % _page)
            _config = config()
            _config.bing()
            
            _source = url.replace('https', '').replace('http', '').replace(':', '').replace('//', '').replace('www.', '')
            if _source.find('/') != -1:
                _source = _source[:_source.find('/')]
                
            _url = _config.bing_settings['externallinks'].replace('[URL]', url).replace('[BASE_URL]', _source )
            _base = _url
            
            _html = self.external_links(_url, 'BING')
            _repository = _html.backlinks
            
            print("Extracted Back Links: %s" % _repository)
            _position = len(_repository)
            _lastchange = _page
            while _html.next != '':
                if _page == 500 or _lastchange == _page - 100:
                    break
                
                _position += 1
                time.sleep(3)
                _html = self.external_links(_base + _iteration.replace("[ITERATION_STEP]", str( _position )), 'BING')                     
                for _link in _html.backlinks:
                    if _link not in _repository:
                        _repository.append(_link)
                        _lastchange = _page
                        
                _page += 1
                _position += len(_html.backlinks)
                print("Page = %i & Links = %i" % (_page, len(_html.backlinks)))
                
            print("Total Links = %i" % len(_repository))
            
        except request.URLError as e:
            print("Error: %s" % e.reason )
        except ValueError as v:
            print("Non urllib Error: %s" % v)
            
        return len(_repository)
    
    def getLinks(self, query, useAPI = False):
        # Obtain API Settings
        _config = config()
        _config.bing()

        try:            
            # Keywords
            _keywords = []
            for _synonyms in wordnet.synsets(query):
                for _s in _synonyms.lemmas():
                    _keywords.append(_s.name().replace('_', ' '))

            # Set Repository Structure
            _name = os.getcwd()+'\\BING\\'+query+'_'+time.strftime("%Y%m%d%H%M%S")+".data"
            _file = open( _name, "w" )   
            _file.write('index\turl\tdescription\tdiv\th1\th2\th3\th4\th5\th6\tinbound_links\tkeywords\toutbound_links\tp\troot\tspan\ttitle\n')
            _file.close()

            # Direct Call
            _html = self.extract_links(_config.bing_settings['url']+query, 'BING')
            _indexValue = 0
            for _entry in _html.links:
                _indexValue += 1
                if '.pdf' not in _entry:
                    print("Searching: %s" % _entry.get('url'))
                    _indexes = sorted(self.extract_indexes(_entry.get('url'), _keywords ).items())
                    if _indexes:
                        _file = open(_name, 'a')
                        _file.write(str(_indexValue) + '\t' + _entry.get('url') )
                        for _index in _indexes:
                            _file.write('\t'+str(_index[1]))
                        _file.write('\n')    
                        _file.close()

        except request.URLError as e:
            print("Error: %s" % e.reason )
        except ValueError as v:
            print("Non urllib Error: %s" % v)
            
                