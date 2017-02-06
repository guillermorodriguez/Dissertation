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
import os

class Extract:
    
    _proxies = []
    _agents = []
    
    def __init__(self):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__ )
        print('==================================================================')
    
        _proxies = []
        _source = os.path.dirname(os.path.realpath(__file__)) + '\\proxies.txt'  
        with open(_source, 'r') as _file:
            for _line in _file:
                _proxies.append(_line.strip())
    
    # Retrieve series of links from search engine query
    def extract_links(self, url, engine, use_proxy = False):
        _html = HTMLhelper()
        _html.search_engine(engine, 'URLS')  
                            
        try:            
            if len( self._agents ) == 0:
                _source = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'agents.txt'
                _file = open(_source, 'r')
                _agent = _file.readline().strip()
                while _agent:
                    self._agents.append(_agent)
                    _agent = _file.readline().strip()
                _file.close() 
            
            _request = None
            url = url.replace(' ', '%20')
            if use_proxy:                
                if len(self._proxies) == 0:
                    _source = os.path.dirname(os.path.realpath(__file__)) + '\\proxies.txt'  
                    with open(_source, 'r') as _file:
                        for _line in _file:
                            self._proxies.append(_line.strip())
                
                _prox = random.choice(self._proxies)
                print("Using Proxy: %s" % _prox)      
                
                proxies = {'http': 'http://'+_prox}
                opener = urllib.request.FancyURLopener(proxies)
                with opener.open(url) as f:
                    print(f.read().decode('utf-8'))
                
                
#                proxy_support = urllib.request.ProxyHandler({'http' : _prox })
#                opener = urllib.request.build_opener(proxy_support)
#                opener.addheaders = [random.choice(self._agents)]
#                urllib.request.install_opener(opener)
#                with urllib.request.urlopen(url) as response:
#                    _html.feed(response.read().decode('utf-8'))
            else:    
                _request = urllib.request.Request(url)                
                if engine.upper() == 'YAHOO' or engine.upper() == 'GOOGLE':
                    _request.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
                else:
                    _request.add_header('User-Agent', random.choice(self._agents))           
                _response = urllib.request.urlopen(_request)                     
                _html.feed( _response.read().decode('utf-8') )            
        except ValueError as v:
            print("Error: %s" % v)
            exit()
            
        return _html
    
    # Extract indexes from end point URL given keywords array
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
    
    # Extract embedded links from search engine
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
            
#            while _html.need_proxy:
#                _proxy = random.choice(self._proxies)
#                print("Using Proxy: %s" % _proxy)
#                
#                _request = urllib.request.Request(url, proxies={'http': _proxy})
#                _request.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
#                _response = urllib.request.urlopen(_request, timeout=180)     
#
#                _html.get_backlinks(url, engine)
#                _html.feed(_response.read().decode('utf-8'))
            
        except:
            print(sys.exc_info()[1])
            return {}
        return _html