"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015
    @Requires:      Bing Search API
                        https://datamarket.azure.com/dataset/bing/search#schema                    
    @Purpose:       The purpose of this class is to perform a query through the Bing Search API and retrieve a response 
                    object by way of XML. This data set is then parsed to qualify search result URLs for further processing.                        
"""

import sys
from config import *
import urllib.request as request
from xml.dom import minidom
from htmlHelper import *
from extract import *
import time
import os

class pyBing(Extract):
    
    def __init__(self, query):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')
        
        # Obtain API Settings
        _config = config()
        _config.bing()
        
        try:            
            # Keywords
            _keywords = {}
            _keywords[query] = ''
            
            # Set Repository Structure
            _name = os.getcwd()+'\\BING\\'+query+'_'+time.strftime("%Y%m%d%H%M%S")+".data"
            _file = open( _name, "w" )   
            _file.write('index\turl\tdescription\tdiv\th1\th2\th3\th4\th5\th6\tinbound_links\tkeywords\toutbound_links\tp\troot\tspan\ttitle\n')
            _file.close()
            
            _query = _config.bing_settings['url_api'] + request.quote("'%s'" % query)
            _passmgr = request.HTTPPasswordMgrWithDefaultRealm()
            _passmgr.add_password(None, _query, _config.bing_settings['id'], _config.bing_settings['key'])

            _handle = request.HTTPBasicAuthHandler(_passmgr)

            _opener = request.build_opener(_handle)
            _opener.open(_query)

            request.install_opener(_opener)

            _response = request.urlopen(_query)

            _html = HTMLhelper()
            _html.search_engine('BING', 'URLS')
            _html.feed( _response.read().decode("utf-8") )
            _indexValue = 0
            for _entry in _html.links:
                _indexValue += 1
                print("Searching: %s" % _entry)
                _indexes = sorted(self.extract_indexes(_entry, _keywords ).items())
                if _indexes:
                    _file = open(_name, 'a')
                    _file.write(str(_indexValue) + '\t' + _entry )
                    for _index in _indexes:
                        _file.write('\t'+str(_index[1]))
                    _file.write('\n')    
                    _file.close()

        except request.URLError as e:
            print("Error: %s" % e.reason )
        except ValueError as v:
            print("Non urllib Error: %s" % v)
        
        
        
        
        
        
        
        