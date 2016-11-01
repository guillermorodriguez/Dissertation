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
    def __init__(self, query):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')

        # Obtain API Settings
        _config = config()
        _config.google()

        try:
            _html = self.extract_links(_config.google_settings['url']+query, 'GOOGLE')
           
            response = requests.get(url, headers=headers)
            data = response.content
            print(data)
            parser = htmlHelper()
            #parser.set_keywords({'service', 'management'})
            parser.set_url(url)
            parser.feed(response.content)
            
            
            
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        