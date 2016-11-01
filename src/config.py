"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015
    @Purpose:       The purpose of this program module is to read the configuration 
                    settings for each search engine. Configuration settings include
                    items such as:
                        bing = { key: '', id: '', url: '' }
                        google = {}
                        yahoo = { clientID: '', clientSecret: '', url: '' }
"""

from xml.dom import minidom
import os

class config:
    
    bing_settings = { 'key': '', 'id': '', 'url': '', 'url_api': ''}
    yahoo_settings = { 'url': ''}
    google_settings = { 'url': '' }

    def __init__(self):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__  )
        print('==================================================================')
        
        self.file = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'config.xml'
        self.xmldoc = minidom.parse(self.file)
    
    def bing(self):
        for child in self.xmldoc.getElementsByTagName("bing")[0].childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                self.bing_settings[child.nodeName] = child.firstChild.nodeValue

    def google(self):
        for child in self.xmldoc.getElementsByTagName("google")[0].childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                self.google_settings[child.nodeName] = child.firstChild.nodeValue
            
    def yahoo(self):
        for child in self.xmldoc.getElementsByTagName("yahoo")[0].childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                self.yahoo_settings[child.nodeName] = child.firstChild.nodeValue