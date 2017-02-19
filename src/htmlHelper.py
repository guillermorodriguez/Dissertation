from html.parser import HTMLParser
import re
"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015
    @Requires:                          
    @Purpose:                               
"""
class HTMLhelper(HTMLParser):
        
    """
        type = BING | GOOGLE | YAHOO
        operation = URLS | KEYS | INDEX
                    URLS = Links on search engine
                    KEYS = Primary indexing attributes on result link for each individual link extracted from main query to search engine
                    INDEX = Backlinks to main URL
    """
    
    indexes = { 'description': 0, 'div': 0, 'outbound_links': 0, 'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0, 'inbound_links': 0, 'keywords': 0, 'p': 0, 'span': 0, 'title': 0, 'root': 0 }
    links = []
    operation = ''
    next = ''
    root_url = ''
    tag = ''
    type = ''
    url = ''
    words = {}    
    backlinks = []
    need_proxy = False    
 
    # Extract links from search engine query. Base search to retrieve series of URLs that match a given query to search engine.
    # operation = URLS
    def search_engine(self, type, operation):
        self.links = []
        self.operation = operation               
        self.next = ''
        self.type = type      
        self.need_proxy = False
        self.previous_tag = ''
    
    # Retrieve individual indexes from keywords for a specific end point, i.e. URL
    # operation = KEYS
    def search_indexes(self, url, operation, words):
        self.indexes = { 'description': 0, 'div': 0, 'outbound_links': 0, 'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0, 'inbound_links': 0, 'keywords': 0, 'p': 0, 'span': 0, 'title': 0, 'root': 0 }
        self.operation = operation
        self.url = url      
        self.root_url = self.url.lower().replace('https', '').replace('http', '').replace(':', '').replace('//', '').replace('www.', '')
        self.words = words
        self.need_proxy = False
        
        for _word in self.words:  
            if len(self.root_url) > 0:
                self.indexes['root'] += ( self.root_url.lower().count(_word.lower()) * len(_word) ) / len(self.root_url) 

    # Get backlinks to main URL found from the invocation of the search_engine(). 
    def get_backlinks(self, url, type):
        self.url = url
        self.next = ''
        self.type = type
        self.backlinks = []
        self.operation = 'INDEX'
        self.need_proxy = False
        
    def handle_starttag(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs
        if self.operation.upper() == 'URLS':
            if self.tag == 'a' and self.type.upper() == 'GOOGLE':
                if len(attrs) == 2:
                    _hasMouseDown = False
                    _hasHref = False
                    _link = ''
                    _iterate = True
                    for items in attrs:
                        for key in items:
                            if _iterate:
                                if 'href' in key and items[1].strip() != '#' and ('google' not in items[1].strip() and items[1][0] != '/'):
                                    _hasHref = True
                                    _link = items[1]
                                elif 'onmousedown' in key and 'return' in items[1] and 'rwt(this' in items[1]:
                                    _hasMouseDown = True
                                elif ('class' == key.strip() and 'fl' == items[1].strip()) or ('data-' in key.strip()):
                                    _hasMouseDown = False
                                    _hasHref = False
                                    _iterate = False
                    if _hasHref and _hasMouseDown:
                        self.links.append({'url': _link, 'count': len(self.links) + 1 })   
                else:
                    _hasClass = False
                    _hasHref = False
                    _hasId = False
                    _link = ''
                    for items in attrs:
                        for key in items:
                            if 'class' in key and 'pn' in items[1]:
                                _hasClass = True
                            elif 'href' in key:
                                _hasHref = True
                                _link = items[1]
                            elif 'id' in key and 'pnnext' in items[1]:
                                _hasId = True
                    if _hasClass and _hasHref and _hasId and _link != '':
                        self.next = 'https://www.google.com'+_link
                    
            elif self.tag == 'a' and self.type.upper() == 'BING':
                _hasHref = False
                _hasH = False
                _hasTitle = False
                _hasClass = False
                _link = ''
                for items in attrs:
                    for key in items:
                        if 'href' == key and ('bing.com' not in items[1] ) and ('go.microsoft.com' not in items[1] ) and items[1][0] != '/' and 'javascript:' not in items[1] and '#' != items[1][0]:
                            _hasHref = True
                            _link = items[1]
                        elif 'h' == key and 'Ads' not in items[1].strip():
                            _hasH = True
                        elif 'title' == key and 'next page' == items[1].strip().lower():
                            _hasTitle = True
                        elif 'class' == key and 'sb_pagn' == items[1].strip().lower():
                            _hasClass = True
                        elif 'href' == key and '/search?q=' == items[1][:10].strip().lower() and '&first=' in items[1] and 'FORM=PORE' in items[1]:
                            _hasHref = True
                            _link = 'http://www.bing.com' + items[1]
                if _hasHref and _hasH and (not _hasTitle) and (not _hasClass):
                    _exists = False
                    for _element in self.links:
                        if 'url' in _element and ( _element.get('url').strip().lower().replace('https', '').replace('http','') == _link.strip().lower().replace('https', '').replace('http','') or _link.strip().lower().replace('https', '').replace('http','') in _element.get('url').strip().lower().replace('https', '').replace('http','') or _element.get('url').strip().lower().replace('https', '').replace('http','') in _link.strip().lower().replace('https', '').replace('http','')):
                            _exists = True
                            break
                    if not _exists:
                        self.links.append({'url': _link, 'count': len(self.links)+1})              
                elif _hasHref and _hasH and _hasTitle and _hasClass:
                    self.next = _link
                    
            elif self.tag == 'a' and self.type.upper() == 'YAHOO':
                _hasClass = False
                _hasLink = False
                _hasTarget = False
                _hasData = False
                _hasReferrerPolicy = False
                _link = ''
                for items in attrs:
                    for key in items:
                        if 'class' == key:
                            _hasClass = True
                        elif  'href' == key and 'javascript' not in items[1].strip().lower() and '#' not in items[1].strip().lower() and 'search' not in items[1].strip().lower() and 'yahoo.com' not in items[1].strip().lower():
                            _hasLink = True
                            _link = items[1]
                        elif 'referrerpolicy' == key and 'origin' == items[1].strip().lower():
                            _hasReferrerPolicy = True
                        elif 'target' == key:
                            _hasTarget = True
                        elif 'data' in key and 'beacon' in items[1].strip().lower():
                            _hasData = True
                if _hasClass and _hasLink and _hasTarget and _hasData and _hasReferrerPolicy:                    
                    self.links.append({'url': _link, 'count': len(self.links) + 1 })                                                           
        elif self.operation.upper() == 'KEYS':
            # Meta Tag Indexes - description and keywords
            if self.tag.lower().strip() == 'meta':
                _attrs = dict(attrs)            
                if 'name' in _attrs and 'content' in _attrs and len(_attrs) == 2:
                    # Meta Tags
                    for _word in self.words:
                        if _attrs['name'].lower().strip() == 'description' and len(_attrs['content'].strip()) > 0:
                            self.indexes['description'] += ( _attrs['content'].lower().count(_word.lower()) * len(_word) ) / len(_attrs['content'].strip())
                        elif _attrs['name'].lower().strip() == 'keywords' and len(_attrs['content'].strip()) > 0:
                            self.indexes['keywords'] += (_attrs['content'].lower().count(_word.lower()) * len(_word) ) / len(_attrs['content'].strip())
            elif self.tag.lower().strip() == 'a':
                # Outbound Links
                _nofollow = False
                _validLink = False
                for items in attrs:
                    for key in items:
                        _baseURL = self.root_url
                        if self.root_url.find('/') != -1:
                            _baseURL = self.root_url[:self.root_url.find('/')]
                        if 'href' == key and _baseURL not in items[1] and '#' != items[1][:1] and '/' != items[1][:1] and 'javascript' not in items[1]:
                            _validLink = True
                        elif 'rel' == key and items[1].strip().lower() == '':
                            _nofollow = True
                if not _nofollow and _validLink:
                    self.indexes['outbound_links'] += 1                    
        elif self.operation.upper() == 'INDEX':
            if self.tag == 'a' and self.type.upper() == 'BING':
                _hasHref = False
                _hasH = False
                _hasTitle = False
                _hasClass = False
                _link = ''
                for items in attrs:
                    for key in items:
                        if 'href' == key.lower() and ('bing.com' not in items[1] ) and ('go.microsoft.com' not in items[1] ) and items[1][0] != '/' and 'javascript:' not in items[1] and '#' != items[1][0]:
                            _hasHref = True
                            _link = items[1]
                        elif 'h' == key.lower() and 'ID=SERP' in items[1].strip():
                            _hasH = True
                        elif 'class' == key.lower() and 'sb_pagn' == items[1].strip().lower():
                            _hasClass = True
                        elif 'title' == key.lower() and 'next page' == items[1].strip().lower():
                            _hasTitle = True
                        elif 'href' == key.lower() and '/search?q=' in items[1].strip().lower() and ( 'FORM=' not in items[1] ) and ('bing.com' not in items[1]) :
                            _hasHref = True
                            self.next = items[1]
                if _hasHref and _hasH:
                    _exists = False
                    if ( not _hasTitle ) and ( not _hasClass ):
                        for _element in self.backlinks:
                            if ( _element.strip().lower().replace('https', '').replace('http','') == _link.strip().lower().replace('https', '').replace('http','') or _link.strip().lower().replace('https', '').replace('http','') in _element.strip().lower().replace('https', '').replace('http','') or _element.strip().lower().replace('https', '').replace('http','') in _link.strip().lower().replace('https', '').replace('http','')):
                                _exists = True
                                break
                        if not _exists:
                            self.backlinks.append(_link)                                  
                    
            elif self.tag == 'a' and self.type.upper() == 'GOOGLE':
                # Extract Links for Backlink Analysis
                if len(attrs) == 2:
                    _hasMouseDown = False
                    _hasHref = False
                    _link = ''
                    _iterate = True
                    for items in attrs:
                        for key in items:
                            if _iterate:
                                if 'href' in key and items[1].strip() != '#' and ('google' not in items[1].strip() and items[1][0] != '/'):
                                    _hasHref = True
                                    _link = items[1]
                                elif 'onmousedown' in key and 'return' in items[1] and 'rwt(this' in items[1]:
                                    _hasMouseDown = True
                                elif ('class' == key.strip() and 'fl' == items[1].strip()) or ('data-' in key.strip()):
                                    _hasMouseDown = False
                                    _hasHref = False
                                    _iterate = False
                    if _hasHref and _hasMouseDown:
                        self.backlinks.append(_link)   
                else:
                    _hasClass = False
                    _hasHref = False
                    _hasId = False
                    _link = ''
                    for items in attrs:
                        for key in items:
                            if 'class' in key and 'pn' in items[1]:
                                _hasClass = True
                            elif 'href' in key:
                                _hasHref = True
                                _link = items[1]
                            elif 'id' in key and 'pnnext' in items[1]:
                                _hasId = True
                    if _hasClass and _hasHref and _hasId and _link != '':
                        self.next = 'https://www.google.com'+_link               
                                
            elif self.tag == 'a' and self.type.upper() == 'YAHOO':
                _hasClass = False
                _hasLink = False
                _hasTarget = False
                _hasData = False
                _hasReferrerPolicy = False
                _link = ''
                for items in attrs:
                    for key in items:
                        if 'class' == key:
                            _hasClass = True
                        elif  'href' == key and 'javascript' not in items[1].strip().lower() and '#' not in items[1].strip().lower() and 'search' not in items[1].strip().lower() and 'yahoo.com' not in items[1].strip().lower():
                            _hasLink = True
                            _link = items[1]
                        elif 'referrerpolicy' == key and 'origin' == items[1].strip().lower():
                            _hasReferrerPolicy = True
                        elif 'target' == key:
                            _hasTarget = True
                        elif 'data' in key and 'beacon' in items[1].strip().lower():
                            _hasData = True
                if _hasClass and _hasLink and _hasTarget and _hasData and _hasReferrerPolicy:                    
                    self.backlinks.append(_link)                   
                    
    def handle_endtag(self, tag):
        self.tag = ''

    def handle_data(self, data):        
        # Search Engine Prevents Response
        if self.type.upper() == 'BING':
            pass
        elif self.type.upper() == 'GOOGLE':
            pass
        elif self.type.upper() == 'YAHOO':
            if 'error 999' in data:
                print("Proxy Required")
                self.need_proxy = True
                
        if self.operation.upper() == 'URLS':
            # Extract Search Engine URLS
            if self.tag == 'd:url' and self.type.upper() == 'BING':
                pass
            elif self.tag == 'a' and self.type.upper() == 'GOOGLE':
                pass
            elif self.tag == 'a' and self.type.upper() == 'YAHOO':
                if data == 'Next':
                    _hasLink = False
                    for items in self.attrs:
                        for key in items:
                            if key == 'href':
                                self.next = items[1]
        elif self.operation.upper() == 'KEYS':
            # Keywords in Text Tag Elements - div, h1, h2, h3, h4, h5, h6, p, span, title
            for _key in self.indexes:
                if _key == self.tag:
                    for _word in self.words:    
                        if len(data.strip()) > 0:
                            self.indexes[_key] += ( data.lower().count(_word.lower()) *len(_word) ) / len(data.strip()) 
        elif self.operation.upper() == 'INDEX':   
            # Backlinks - Next Link on Page
            if self.type.upper() == 'BING':
                # Found in Anchor Tag
                pass
            elif self.type.upper() == 'GOOGLE':
                pass
            elif self.type.upper() == 'YAHOO':
                if data == 'Next':
                    _hasLink = False
                    for items in self.attrs:
                        for key in items:
                            if key == 'href':
                                self.next = items[1]