#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    Utility to add Transkribus documents to another collection

    JL Meunier - Nov 2016


    Copyright Xerox(C) 2016 H. Déjean, JL. Meunier

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    
    Developed  for the EU project READ. The READ project has received funding 
    from the European Union’s Horizon 2020 research and innovation programme 
    under grant agreement No 674943.

"""

#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os, logging
from optparse import OptionParser

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from common.trace import traceln, trace
from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit
from TranskribusPyClient.client import TranskribusClient

DEBUG = 0

description = """Add one or several documents stored in Transkribus to another Transkribus collection.
Document(s) and collection are specified by their unique identifier (a number).
""" + _Trnskrbs_description

usage = """%s <colId>  [ <docId> | <docIdFrom>-<docIdTo> ]+
Documents are specified by a space-separated list of numbers, or number ranges, e.g. 3-36.
"""%sys.argv[0]

class DoAddDocToCollec(TranskribusClient):
    """
    Add a document to another collection.
    """
    
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=_Trnskrbs_default_url, proxies=sHttpProxy, loggingLevel=loggingLevel)
        

if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, _Trnskrbs_default_url)
        
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}
    # ------------------------------------------------------------------------------------------------
    doer = DoAddDocToCollec(options.server, proxies, loggingLevel=logging.INFO)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    
    # --- 
    #target collection
    try:                    colId = int(args.pop(0))
    except Exception as e:  _exit(usage, 1, e)

    # --- 
    # document list
    try:
        lDocId = []
        while args:
            chunk = args.pop(0).strip()
            li = chunk.split('-')
            if li and len(li) == 2:
                docId1, docId2 = [int(i) for i in li]
                lDocId.extend( range(docId1,docId2+1) )
            else:
                docId = int(chunk)
                lDocId.append(docId)
    except Exception as e:
        _exit(usage, 2, e)

    # ---   
    #credentials and proxy
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}



    # ------------------------------------------------------------------------------------------------
    doer = DoAddDocToCollec(options.server, proxies, loggingLevel=logging.INFO)

    __Trnskrbs_do_login_stuff(doer, options, trace, traceln)
    
    trace("- adding to collection '%d' the %d documents: "%(colId, len(lDocId)))
    for docId in lDocId:
        trace(" %d"%docId)
        try:
            doer.collections_addDocToCollection(colId, docId)
        except Exception as e:
            traceln()
            traceln("ERROR: could not add document '%d' to collection '%d'"%(docId, colId))
            raise e
    traceln()      
    traceln("- Done for %d documents"%len(lDocId))
    
