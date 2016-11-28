"""
    @Author:        Guillermo Rodriguez
    @Date:          September 19, 2016
    @Requires:      
    @Purpose:       
"""
import urllib.request
from htmlHelper import *
import sys
import random

class Extract:
    
    _proxies = []
    
    def __init__(self):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')
    
        _file = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'proxies.txt'
        _proxy = _file.readline().strip()
        while _proxy:
            self._proxies.append(_proxy)
            _proxy = _file.readline().strip()
        _file.close() 
        
    def extract_links(self, url, engine):
        _html = HTMLhelper()
        try:
            _request = urllib.request.Request(url.replace(' ', '%20'))
            _request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
            _response = urllib.request.urlopen(_request)
            
            _html.search_engine(engine, 'URLS')            
            _html.feed( _response.read().decode('utf-8')  )
        except ValueError as v:
            print("Error: %s" % v)
            
        return _html
    
    def extract_indexes(self, url, keywords):
        _html = HTMLhelper()
        try:
            _request = urllib.request.Request(url.replace(' ', '%20'))
            _request.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')            
            _response = urllib.request.urlopen(_request, timeout=180)     

            _html.search_indexes(url, 'KEYS', keywords)
            _html.feed(_response.read().decode('utf-8'))
        except:
            print(sys.exc_info()[1])
            return {}
        return _html.indexes
    
    def external_links(self, url, engine):
        _html = HTMLhelper()
        try:

            url = url.replace(' ', '%20')
            print("Back Links: %s" % url)
            _request = urllib.request.Request(url)
            _request.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
            _response = urllib.request.urlopen(_request, timeout=180)     

            _html.get_backlinks(url, engine)
            _html.feed(_response.read().decode('utf-8'))
            
            while _html.need_proxy:
                _proxy = random.choice(self.proxies)
                print("Using Proxy: %s" % _proxy)
                
                _request = urllib.request.Request(url, proxies={'http': _proxy})
                _request.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
                _response = urllib.request.urlopen(_request, timeout=180)     

                _html.get_backlinks(url, engine)
                _html.feed(_response.read().decode('utf-8'))
            
        except:
            pass
        return _html