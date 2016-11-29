#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    Utility to duplicate Transkribus documents from a collection to another collection

    JL Meunier - Nov 2016


    Copyright Xerox(C) 2016 H. DÃ©jean, JL. Meunier

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
    from the European Unionâ€™s Horizon 2020 research and innovation programme 
    under grant agreement No 674943.

"""

#    TranskribusCommands/do_copyDocToCollec.py 3571 3820 8251 8252


#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os, logging
from optparse import OptionParser

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit
from TranskribusPyClient.client import TranskribusClient, getStoredCredentials
from common.trace import traceln, trace

DEBUG = 0

description = """Copy (duplicate) one or several documents stored in a Transkribus collection to another Transkribus collection.
Document(s) and collections are specified by their unique identifier (a number).
""" + _Trnskrbs_description

usage = """%s <from_colId>  <to_colId> [ <docId> | <docIdFrom>-<docIdTo> ]+
Documents are specified by a space-separated list of numbers, or number ranges, e.g. 3-36.
"""%sys.argv[0]

class DoCopyDocToCollec(TranskribusClient):
    """
    Copy a document from a collection to another
    """
    sDefaultServerUrl = _Trnskrbs_default_url
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
        

if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoCopyDocToCollec.sDefaultServerUrl)
        
    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    #source collection
    try:                        colIdFrom = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
    #target collection
    try:                        colIdTo   = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)

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

    # ------------------------------------------------------------------------------------------------
    doer = DoCopyDocToCollec(options.server, proxies, loggingLevel=logging.INFO)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)


    #the only issue is that we need to have the name of each document...
    traceln("- checking existence of each document in source collection '%d'"%(colIdFrom))
    dName_by_docId = {}
    lDocDic = doer.collections_list(colIdFrom)
    for docDic in lDocDic:
        dName_by_docId[ docDic['docId'] ] = docDic['title']
    #check now, so as to avoid partial copies...
    for docId in lDocId:
        try:
            name = dName_by_docId[docId]
        except KeyError as e:
            traceln()
            traceln("ERROR: document '%d' is not in source collection '%d'"%(docId, colIdFrom))
            _exit("", 3, e)
    
    trace("- copying from collection %d to collection '%d' the %d documents: "%(colIdFrom, colIdTo, len(lDocId)))
    for docId in lDocId:
        name = dName_by_docId[docId]
        trace(" %d  ('%s')"%(docId, name))
        try:
            doer.collections_copyDocToCollection(colIdFrom, docId, colIdTo, name)
        except Exception as e:
            traceln()
            traceln("ERROR: could not copy document '%d' from collection '%d' to collection '%d'"%(docId, colIdFrom, colIdTo))
            _exit("", 4, e)
    traceln()      
    traceln("- Done for %d documents"%len(lDocId))
    
