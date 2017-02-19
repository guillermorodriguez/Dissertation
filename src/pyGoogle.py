"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015
    @Requires:      
                        
                    
    @Purpose:                               
"""
import sys
from config import *
from rauth import OAuth2Service
import urllib.request
from xml.dom import minidom
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
        _repository = []
        try:
            _config = config()
            _config.google()
            
            _source = url.replace('https', '').replace('http', '').replace(':', '').replace('//', '').replace('www.', '')
            if _source.find('/') != -1:
                _source = _source[:_source.find('/')]
            
            _url = _config.google_settings['externallinks'].replace('[URL]', url).replace('[BASE_URL]', _source )
            
            _html = self.external_links(_url, 'GOOGLE')
            print(_html.backlinks)
            if _html.backlinks:                
                for _link in _html.backlinks:
                    if _link not in _repository:
                        _repository.append(_link)
                        
                print("Total Links = %i" % len(_repository))
            else:
                _repository.append('ERROR')
                print("Error Extracting Data From Google")                                           
            
        except urllib.request.URLError as e:
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

        