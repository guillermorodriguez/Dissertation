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

class pyYahoo():
    
    """ """
    
    def __init__(self, query, results, use_api = True):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')
        
        # Obtain API Settings
        _config = config()
        _config.yahoo()

        try:
            if use_api in ("True", "T", "Yes", "Y", 1, True):
                # API Call
                _params = urllib.parse.urlencode({'q': query, 'sites': '', 'format': 'xml'})
                _headers = {'consumer_key': _config.yahoo_settings['clientID'], 'consumer_secret': _config.yahoo_settings['clientSecret'] }
                _query = _config.yahoo_settings['url_api'] + _params
                
                _request = urllib.request.Request(_query)
                _request.add_header('oauth', urllib.parse.urlencode( _headers ) )
    
                _response = urllib.request.urlopen(_request)
                _content = _response.read()
            else:         
                # Direct Call
                _request = urllib.request.Request(_config.yahoo_settings['url'] + query) 
                _response = urllib.request.urlopen(_request)
               
                
                _html = HTMLhelper()
                _html.engine('YAHOO', 'URLS')
                _html.feed( _response.read().decode("utf-8")  )
                for _entry in _html.links:
                    print(_entry)

        except urllib.request.URLError as e:
            print("Error: %s" % e.reason )
        except ValueError as v:
            print("Non urllib Error: %s" % v)
