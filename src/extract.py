"""
    @Author:        Guillermo Rodriguez
    @Date:          September 19, 2016
    @Requires:      
    @Purpose:       
"""
import urllib.request
from htmlHelper import *

class Extract:
    
    def __init__(self):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')
        
    def extract_links(self, url, engine):
        _html = HTMLhelper()
        try:
            _html.search_engine(engine, 'URLS')
            _html.feed( urllib.request.urlopen(urllib.request.Request(url)).read().decode('utf-8')  )
        except ValueError as v:
            print("Error: %s" % v)
            
        return _html
    
    def extract_indexes(self, url, keywords):
        _html = HTMLhelper()
        try:
            _request = urllib.request.Request(url)
            _request.add_header('User-agent', 'Mozilla/11.0')
            _response = urllib.request.urlopen(_request)     
            
            _html.search_indexes(url, 'KEYS', keywords)
            _html.feed(_response.read().decode('utf-8'))
        except:
            pass
        return _html.indexes