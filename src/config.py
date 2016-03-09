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
    yahoo_settings = { 'clientID': '', 'clientSecret': '', 'url': '', 'url_api': ''}
    google_settings = { 'url': '', 'url_api': '' }

    def __init__(self):
        print('\n==================================================================')
        print( '%s Initialized' % self.__class__.__name__  )
        print('==================================================================')
        
        self.file = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'config.xml'
        self.xmldoc = minidom.parse(self.file)
    
    def bing(self):
        for child in self.xmldoc.getElementsByTagName("bing")[0].childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                if child.nodeName == "key":
                    self.bing_settings['key'] = child.firstChild.data
                elif child.nodeName == "id":
                    self.bing_settings['id'] = child.firstChild.nodeValue
                elif child.nodeName == "url":
                    self.bing_settings['url'] = child.firstChild.nodeValue
                elif child.nodeName == "url_api":
                    self.bing_settings['url_api'] = child.firstChild.nodeValue


    def google(self):
        for child in self.xmldoc.getElementsByTagName("google")[0].childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                if child.nodeName == "url":
                    self.google_settings['url'] = child.firstChild.nodeValue
                elif child.nodeName == "url_api":
                    self.google_settings['url_api'] = child.firstChild.nodeValue
            
    def yahoo(self):
        for child in self.xmldoc.getElementsByTagName("yahoo")[0].childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                if child.nodeName == "clientID":
                    self.yahoo_settings['clientID'] = child.firstChild.data
                elif child.nodeName == "clientSecret":
                    self.yahoo_settings['clientSecret'] = child.firstChild.nodeValue
                elif child.nodeName == "url":
                    self.yahoo_settings['url'] = child.firstChild.nodeValue
                elif child.nodeName == "url_api":
                    self.yahoo_settings['url_api'] = child.firstChild.nodeValue