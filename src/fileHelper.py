"""
    @Author:        Guillermo Rodriguez
    @Date:          July 14, 2015
    @Requires:      Bing Search API
                        https://datamarket.azure.com/dataset/bing/search#schema                    
    @Purpose:       The purpose of this class is to perform a query through the Bing Search API and retrieve a response 
                    object by way of XML. This data set is then parsed to qualify search result URLs for further processing.                        
"""

import sys
from config import *
import urllib.request
from xml.dom import minidom
from htmlHelper import *

class fileHelper():
    
    def __init__(self):
        print('\n==================================================================')
        print( self.__class__.__name__ + ' Class Initialized')
        print('==================================================================')
        
    def write_urls(self, engine, urls):
        pass
    
    


