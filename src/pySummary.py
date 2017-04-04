"""
    @Author:        Guillermo Rodriguez
    @Date:          April 1, 2015
    @Purpose:       The purpose of this algorithm is to determine the minimum, maximum, and average for a series 
                    of entries in a predetermined output file. 
"""
import sys
import argparse
import os

print("Starting Summary Calculations ......")

parser = argparse.ArgumentParser(prog='pySummary.py')
parser.add_argument('-engine', help='Search Engine [BING | GOOGLE | YAHOO]')
parser.add_argument('-file', help='Input File Name')
parse = parser.parse_args()

# --------------------------------------------------------------------------
# Global Configuration
# --------------------------------------------------------------------------
_MODE = "DEBUG"

if parse.engine and parse.file:
    _source = os.getcwd()+"\\"+parse.engine.upper()+"\\data\\"+parse.file
    
    if _MODE == "DEBUG":
        print("Engine: %s" % parse.engine)
        print("File: %s" % _source)

    _max = {'description': 0.0, 'div': 0.0, 'h1': 0.0, 'h2': 0.00, 'h3': 0.0, 'h4': 0.0, 'h5': 0.0, 'h6': 0.0, 'inbound_links': 0.0, 'keywords': 0.0, 'outbound_links': 0.0, 'p': 0.0, 'root': 0.0, 'span': 0.0, 'title': 0.0, 'quality': 0.00}
    _min = {'description': 1000.0, 'div': 1000.0, 'h1': 1000.0, 'h2': 1000.00, 'h3': 1000.0, 'h4': 1000.0, 'h5': 1000.0, 'h6': 1000.0, 'inbound_links': 1000.0, 'keywords': 1000.00, 'outbound_links': 1000.0, 'p': 1000.0, 'root': 1000.0, 'span': 1000.0, 'title': 1000.0, 'quality': 1000.00}
    _totals = {'description': 0.0, 'div': 0.0, 'h1': 0.0, 'h2': 0.00, 'h3': 0.0, 'h4': 0.0, 'h5': 0.0, 'h6': 0.0, 'inbound_links': 0.0, 'keywords': 0.0, 'outbound_links': 0.0, 'p': 0.0, 'root': 0.0, 'span': 0.0, 'title': 0.0, 'quality': 0.00}
    _lines = 0
    _show_quality = False
    if os.path.exists(_source):
        with open(_source, 'r') as _file:
         for _line in _file:
            _data = _line.strip().split('\t')
            
            if len(_data) == 19 : _show_quality = True
            
            if _data[0].upper() != "INDEX":
                _lines += 1
                # Totals
                _totals['description'] = float(_data[3]) 
                _totals['div'] += float(_data[4])
                _totals['h1'] += float(_data[5])
                _totals['h2'] += float(_data[6])
                _totals['h3'] += float(_data[7])
                _totals['h4'] += float(_data[8])
                _totals['h5'] += float(_data[9])
                _totals['h6'] += float(_data[10])
                _totals['inbound_links'] += float(_data[11])
                _totals['keywords'] += float(_data[12])
                _totals['outbound_links'] += float(_data[13])
                _totals['p'] += float(_data[14])
                _totals['root'] += float(_data[15])
                _totals['span'] += float(_data[16])
                _totals['title'] += float(_data[17])
                
                if len(_data) == 19: _totals['quality'] += float(_data[18])
                
                # Maximum
                if float(_data[3]) > _max['description']: _max['description'] = float(_data[3])
                if float(_data[4]) > _max['div']: _max['div'] = float(_data[4])
                if float(_data[5]) > _max['h1']: _max['h1'] = float(_data[5])
                if float(_data[6]) > _max['h2']: _max['h2'] = float(_data[6])
                if float(_data[7]) > _max['h3']: _max['h3'] = float(_data[7])
                if float(_data[8]) > _max['h4']: _max['h4'] = float(_data[8])
                if float(_data[9]) > _max['h5']: _max['h5'] = float(_data[9])
                if float(_data[10]) > _max['h6']: _max['h6'] = float(_data[10])
                if float(_data[11]) > _max['inbound_links']: _max['inbound_links'] = float(_data[11])
                if float(_data[12]) > _max['keywords']: _max['keywords'] = float(_data[12])
                if float(_data[13]) > _max['outbound_links']: _max['outbound_links'] = float(_data[13])
                if float(_data[14]) > _max['p']: _max['p'] = float(_data[14])
                if float(_data[15]) > _max['root']: _max['root'] = float(_data[15])
                if float(_data[16]) > _max['span']: _max['span'] = float(_data[16])
                if float(_data[17]) > _max['title']: _max['title'] = float(_data[17])
                if ( len(_data) == 19 ) and ( float(_data[18]) > _max['quality'] ): _max['quality'] = float(_data[18])
                
                # Minimum
                if float(_data[3]) < _min['description']: _min['description'] = float(_data[3])
                if float(_data[4]) < _min['div']: _min['div'] = float(_data[4])
                if float(_data[5]) < _min['h1']: _min['h1'] = float(_data[5])
                if float(_data[6]) < _min['h2']: _min['h2'] = float(_data[6])
                if float(_data[7]) < _min['h3']: _min['h3'] = float(_data[7])
                if float(_data[8]) < _min['h4']: _min['h4'] = float(_data[8])
                if float(_data[9]) < _min['h5']: _min['h5'] = float(_data[9])
                if float(_data[10]) < _min['h6']: _min['h6'] = float(_data[10])
                if float(_data[11]) < _min['inbound_links']: _min['inbound_links'] = float(_data[11])
                if float(_data[12]) < _min['keywords']: _min['keywords'] = float(_data[12])
                if float(_data[13]) < _min['outbound_links']: _min['outbound_links'] = float(_data[13])
                if float(_data[14]) < _min['p']: _min['p'] = float(_data[14])
                if float(_data[15]) < _min['root']: _min['root'] = float(_data[15])
                if float(_data[16]) < _min['span']: _min['span'] = float(_data[16])
                if float(_data[17]) < _min['title']: _min['title'] = float(_data[17])
                if ( len(_data) == 19 ) and ( float( _data[18] ) < _min['quality'] ): _min['quality'] = float(_data[18])
    else:
        print("Invalid Input File Specified")
    
    if( not _show_quality ): 
        _max.pop('quality', None)
        _min.pop('quality', None)
        _totals.pop('quality', None)
        
    print("MAXIMUM ---------------------------")    
    print(_max)
    print("MINIMUM ---------------------------")
    print(_min)
    print("AVERAGE ---------------------------")
    for key, value in _totals.items():
        _totals[key] = float(value)/_lines
    print(_totals)
else:
    parser.print_help()

print("Ending Summary Calculations ......")