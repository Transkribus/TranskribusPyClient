#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""

    JL Meunier - August 2017


    Copyright Naver(C) 2017 JL. Meunier

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

#    TranskribusCommands/do_LAbatch.py 3571 3820 8251 8252


#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os, logging
from optparse import OptionParser
import json

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit
from TranskribusPyClient.client import TranskribusClient
from common.IntegerRange  import IntegerRange as PageRangeSpec
from common.trace import traceln, trace

DEBUG = 0

description = """Get the TRP of a document
""" + _Trnskrbs_description

usage = """%s <colId> <docId> [<page-ranges>] -n <nb_transcripts>
Return the so-called TRP of all or certain pages, optionally with the given number of transcript(s) per page (-1 means all).

Page range is a comma-separated series of integer or pair of integers separated by a '-' 
For instance 1  or 1,3  or 1-4 or 1,3-6,8
"""%sys.argv[0]

class DoGetDocTrp(TranskribusClient):
    sDefaultServerUrl = _Trnskrbs_default_url
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
    
    def run(self, colId, docId, nrOfTranscripts=1):
        ret = self.getDocById(colId, docId, nrOfTranscripts)
        return ret

if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoGetDocTrp.sDefaultServerUrl)
    parser.add_option("-n", "--n"  , dest='nbTranscript', action="store", type="int", default=1, help="Number of transcripts")
        
    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    doer = DoGetDocTrp(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    # --- 
    try:                        colId = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
    try:                        docId   = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
    try:                        sPageRangeSpec = args.pop(0)
    except Exception as e:      sPageRangeSpec = None
    if args:                    _exit(usage, 2, Exception("Extra arguments to the command"))

    oPageRange = PageRangeSpec(sPageRangeSpec) if sPageRangeSpec else None
        
    # --- 
    # do the job...
    resp = doer.run(colId, docId, nrOfTranscripts=options.nbTranscript)
    if oPageRange:
        traceln("Filtering response as per page specification: %s"%oPageRange)
        #let's filter the response (not super efficient but easy to code...
        ldPages = resp["pageList"]["pages"]
        ldPagesInRange = [ dPage for dPage in ldPages if dPage["pageNr"] in oPageRange]
        resp["pageList"]["pages"] = ldPagesInRange

    print json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': '))
        
    traceln()      
    traceln("- Done")
    
