"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015
    @Requires:      Yahoo - BOSS Search API - https://developer.yahoo.com/boss/search/
                    OAutLib - https://oauthlib.readthedocs.org/en/latest/installation.html
                    pYsearch - http://sourceforge.net/projects/pysearch/

    @Purpose:       The purpose of this class is to perform a query through the Yahoo BOSS Search API and retrieve a response 
                    object by way of XML. This data set is then parsed to qualify search result URLs for further processing.
"""

import sys
from config import *
from rauth import OAuth2Service
import urllib.request
from xml.dom import minidom
from htmlHelper import *
from extract import *

class pyYahoo(Extract):
    
    """ """
    
    def __init__(self, query, results, use_api = True):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')
        
        # Obtain API Settings
        _config = config()
        _config.yahoo()

        try:
            # Direct Call
            _html = self.extract_links(_config.yahoo_settings['url'] + query, 'YAHOO')
            for _entry in _html.links:
                print(_entry)
                print(self.extract_indexes(_entry, {'lubbock'}))

                _html = self.extract_links(_html.next, 'YAHOO')
                for _entry in _html.links:
                    print(_entry)
                    print(self.extract_indexes(_entry, {'lubbock'}))

        except urllib.request.URLError as e:
            print("Error: %s" % e.reason )
        except ValueError as v:
            print("Non urllib Error: %s" % v)

    
