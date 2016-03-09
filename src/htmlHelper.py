from html.parser import HTMLParser

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
    """
    def engine(self, type, operation):
        self.type = type
        self.operation = operation        
        self.links = []
        self.keys = {'DESCRIPTION': 0, 'H1': 0, 'H2': 0, 'H3': 0, 'H4': 0, 'H5': 0, 'H6': 0, 'KEYWORDS': 0, 'P': 0, 'TITLE': 0, 'URL': 0}
        self.totals = {'DESCRIPTION': 0, 'H1': 0, 'H2': 0, 'H3': 0, 'H4': 0, 'H5': 0, 'H6': 0, 'KEYWORDS': 0, 'P': 0, 'TITLE': 0, 'URL': 0}

    def handle_starttag(self, tag, attrs):
        self.tag = tag

        if self.tag == 'a' and self.type.upper() == 'GOOGLE':
            print(attrs)
            print()
        elif self.tag == 'a' and self.type.upper() == 'BING':
            print(attrs)
            print()
        elif self.tag == 'a' and self.type.upper() == 'YAHOO':
            print(attrs)
            print()
        
    def handle_endtag(self, tag):
        self.tag = ''

    def handle_data(self, data):
        if self.operation.upper() == 'URLS':
            if self.tag == 'd:url' and self.type.upper() == 'BING':
                print(data)
                self.links.append( {'url': data} )
            elif self.tag == 'd:url' and self.type.upper() == 'GOOGLE':
                self.links.append( {'url': ''} )
            elif self.tag == 'd:url' and self.type.upper() == 'YAHOO':
                print(data)
                self.links.append( {'url': ''} )