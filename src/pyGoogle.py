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

class pyGoogle(Extract):
    """ 
        
    """
    def __init__(self, query, results, use_api = False):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')

        # Obtain API Settings
        _config = config()
        _config.google()

        try:
            if use_api in ("True", "T", "Yes", "Y", 1, True):
                search = urllib.parse.urlencode ( { 'q' : q } )
                response = urllib.request.urlopen('https://ajax.googleapis.com/ajax/services/search/web?v=1.0&espv=2&rsz=8&' + search ).read()
                _json = json.loads ( response.decode('utf-8') )
                print(response)
                results = _json [ 'responseData' ] [ 'results' ]
                for result in results:
                    title = result['title']
                    url = result['url']   # was URL in the original and that threw a name error exception
                    print ( url )						
            else:
                _html = self.extract_links(_config.google_settings['url'] + query, 'GOOGLE')
                for _entry in _html.links:
                    print(_entry)
                    #print(self.extract_indexes(_entry, {'lubbock'}))
                
                #_request = urllib.request.Request(_config.google_settings['url'] + query)
                #_request.add_header('User-agent', 'Mozilla/11.0')

                #_response = urllib.request.urlopen(_request).read().decode("utf-8")
                #_data = _response[_response.find('<div id="res">'):_response.find('<div id="foot">')] #.encode('ascii', 'ignore')

                #_html = HTMLhelper()
                #_html.search_engine('GOOGLE', 'URLS')
                #_html.feed(_data)
                
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        