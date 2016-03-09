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

class pyBing():
    
    def __init__(self, query, results = 100, use_api = True):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')
        
        # Obtain API Settings
        _config = config()
        _config.bing()
        
        try:
            if use_api in ("True", "T", "Yes", "Y", 1, True):
                _query = _config.bing_settings['url_api'] + request.quote("'%s'" % query)
                _passmgr = request.HTTPPasswordMgrWithDefaultRealm()
                _passmgr.add_password(None, _query, _config.bing_settings['id'], _config.bing_settings['key'])

                _handle = request.HTTPBasicAuthHandler(_passmgr)

                _opener = request.build_opener(_handle)
                _opener.open(_query)

                request.install_opener(_opener)

                _response = request.urlopen(_query)

                _html = HTMLhelper()
                _html.engine('BING', 'URLS')
                _html.feed( _response.read().decode("utf-8") )
                for _entry in _html.links:
                    print(_entry)
            else:
                pass
            
        except request.URLError as e:
            print("Error: %s" % e.reason )
        except ValueError as v:
            print("Non urllib Error: %s" % v)
        
        
        
        
        
        
        
        