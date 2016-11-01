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
                    KEYS = Primary indexing attributes on result links
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
    
    def search_engine(self, type, operation):
        self.links = []
        self.operation = operation               
        self.next = ''
        self.type = type        
        
    def search_indexes(self, url, operation, words):
        self.indexes = { 'description': 0, 'div': 0, 'outbound_links': 0, 'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0, 'inbound_links': 0, 'keywords': 0, 'p': 0, 'span': 0, 'title': 0, 'root': 0 }
        self.operation = operation
        self.url = url      
        self.root_url = self.url.replace('https', '').replace('http', '').replace(':', '').replace('//', '').replace('www.', '').replace('/', '')
        self.words = words
        
        for _word in self.words:  
            if len(self.root_url) > 0:
                self.indexes['root'] += ( self.root_url.lower().replace('-', '').replace('_', '').count(_word.lower().replace(' ', '')) * len(_word.replace(' ', '')) ) / len(self.root_url) 

    def get_backlinks(self, url, type):
        self.url = url
        self.type = type
        
        self.operation = 'INDEX'
        
    def handle_starttag(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs
        if self.operation.upper() == 'URLS':
            if self.tag == 'a' and self.type.upper() == 'GOOGLE':
                print(attrs)
            elif self.tag == 'a' and self.type.upper() == 'BING':
                pass
            elif self.tag == 'a' and self.type.upper() == 'YAHOO':
                _hasClass = False
                _hasLink = False
                _hasTarget = False
                _hasData = False
                _hasReferrer = False
                _link = ''
                for items in attrs:
                    for key in items:
                        if 'class' == key and items[1].strip() != '' and 'thmb' not in items[1]:
                            _hasClass = True
                        elif  'href' == key and items[1].strip() != '#' and 'yahoo' not in items[1].strip().lower() and '/search/' not in items[1].strip().lower():
                            _hasLink = True
                            _link = items[1]
                        elif 'target' == key:
                            _hasTarget = True
                        elif 'data' in key:
                            _hasData = True
                        elif 'referrerpolicy' == key and items[1].strip() == 'origin':
                            _hasReferrer = True
                if _hasClass and _hasLink and _hasTarget and _hasData and _hasReferrer:
                    self.links.append({'url': _link, 'count': len(self.links) + 1 })
        elif self.operation.upper() == 'KEYS':
            if self.tag.lower().strip() == 'meta':
                _attrs = dict(attrs)            
                if 'name' in _attrs and 'content' in _attrs and len(_attrs) == 2:
                    # Meta Tags
                    for _word in self.words:
                        if _attrs['name'].lower().strip() == 'description' and len(_attrs['content']) > 0:
                            self.indexes['description'] += ( _attrs['content'].lower().count(_word.lower()) * len(_word) ) / len(_attrs['content'])
                        elif _attrs['name'].lower().strip() == 'keywords' and len(_attrs['content']) > 0:
                            self.indexes['keywords'] += (_attrs['content'].lower().count(_word.lower()) * len(_word) ) / len(_attrs['content'])
            elif self.tag.lower().strip() == 'a':
                _nofollow = False
                _validLink = False
                for items in attrs:
                    for key in items:
                        if 'href' == key and 'http' in items[1] and self.root_url not in items[1]:
                            _validLink = True
                        elif 'rel' == key and items[1].strip().lower() == '':
                            _nofollow = True
                if not _nofollow and _validLink:
                    self.indexes['outbound_links'] += 1
                    
    def handle_endtag(self, tag):
        self.tag = ''

    def handle_data(self, data):
        if self.operation.upper() == 'URLS':
            # Extract Search Engine URLS
            if self.tag == 'd:url' and self.type.upper() == 'BING':
                if 'http' in data:
                    self.links.append( data )
            elif self.tag == 'd:url' and self.type.upper() == 'GOOGLE':
                self.links.append( {'url': ''} )
            elif self.tag == 'a' and self.type.upper() == 'YAHOO':
                if data == 'Next':
                    _hasLink = False
                    for items in self.attrs:
                        for key in items:
                            if key == 'href':
                                self.next = items[1]
        elif self.operation.upper() == 'KEYS':
            # Keywords in Content Elements
            for _key in self.indexes:
                if _key == self.tag:
                    for _word in self.words:    
                        if len(data) > 0:
                            self.indexes[_key] += ( data.lower().count(_word.lower()) *len(_word) ) / len(data) 
        elif self.operation.upper() == 'INDEX':
            if self.type.upper() == 'BING':
                pass
            elif self.type.upper() == 'GOOGLE':
                pass
            elif self.type.upper() == 'YAHOO':
                pass