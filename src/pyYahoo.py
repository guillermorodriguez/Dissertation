"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015
    @Requires:      
    @Purpose:       The purpose of this class is to perform a query through a native call to the search engine. 
                    This data set is then parsed to qualify search result URLs for further processing.
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

class pyYahoo(Extract):
    
    """ """
    def __init__(self):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')
        
    def getBackLinks(self, url):
        
        _repository = {}
        _page = 1
        _iteration = "&b=[ITERATION_STEP]&pz=10&bct=0&xargs=0"
        try:
            print("Page %i" % _page)
            _config = config()
            _config.yahoo()
            
            _source = url.replace('https', '').replace('http', '').replace(':', '').replace('//', '').replace('www.', '')
            if _source.find('/') != -1:
                _source = _source[:_source.find('/')]
                
            _url = _config.yahoo_settings['externallinks'].replace('[URL]', url).replace('[BASE_URL]', _source )
            _base = _url
            
            _html = self.external_links(_url, 'YAHOO')
            _repository = _html.backlinks
            
            print("Extracted Back Links: %s" % _repository)
            _position = len(_repository)
            _lastchange = _page
            while _html.next != '':
                if _page == 500 or _lastchange == _page - 100:
                    break
                
                _position += 1
                time.sleep(3)
                _html = self.external_links(_base + _iteration.replace("[ITERATION_STEP]", str( _position )), 'YAHOO')                     
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
    
    def getLinks(self, query):
        # Obtain API Settings
        _config = config()
        _config.yahoo()

        try:
            # Keywords
            _keywords = {}
            _keywords[query] = '' 

            # Set Repository Structure
            _name = os.getcwd()+'\\YAHOO\\'+query+'_'+time.strftime("%Y%m%d%H%M%S")+".data"
            _file = open( _name, "w" )   
            _file.write('index\turl\tdescription\tdiv\th1\th2\th3\th4\th5\th6\tinbound_links\tkeywords\toutbound_links\tp\troot\tspan\ttitle\n')
            _file.close()
            # Direct Call        
            _html = self.extract_links(_config.yahoo_settings['url'] + query, 'YAHOO')
            _indexValue = 0
            while _html.next != '':
                for _entry in _html.links:
                    _indexValue += 1
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
                    _html = self.extract_links(_html.next, 'YAHOO') 
                    print("Pausing for 3 seconds")
                    time.sleep(3)

        except urllib.request.URLError as e:
            print("Error: %s" % e.reason )
        except ValueError as v:
            print("Non urllib Error: %s" % v)

            
    
