#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""

    H. Déjean - Dec 2016


    Copyright Xerox(C) 2016 H. Déjean

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
# import json

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit
from TranskribusPyClient.client import TranskribusClient
from common.trace import traceln, trace

DEBUG = 0

description = """Apply Layout Analysis (LA) with batch model.

The syntax for specifying the page range is:
- one or several specifiers separated by a comma
- one separator is a page number, or a range of page number, e.g. 3-8
- Examples: 1   1,3,5   1-3    1,3,5-99,100

""" + _Trnskrbs_description

usage = """%s <colId> <docId> [<pages>] <doNotBlockSeg> <doNotLineSeg>
"""%sys.argv[0]

class DoLAbatch(TranskribusClient):
    sDefaultServerUrl = _Trnskrbs_default_url
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
    
    def run(self, colId, docId, sPages,bBlockSeg,bLineSeq):
        ret = self.analyzeLayoutBatch(colId, docId, sPages,bBlockSeg,bLineSeq)
        return ret

if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoLAbatch.sDefaultServerUrl)
        
    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    doer = DoLAbatch(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    # --- 
    try:                        colId = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
    try:                        docId   = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
    try:                        sPages = args.pop(0)
    except Exception as e:      _exit(usage, 1, e)
    try:                        doNotBlockSeg = int(args.pop(0)) == 0
    except Exception as e:      doNotBlockSeg = False
    try:                        doNotLineSeg = int(args.pop(0)) == 0
    except Exception as e:      doNotLineSeg= False    
    if args:                    _exit(usage, 2, Exception("Extra arguments to the command"))

    # --- 
    # do the job...
    jobid = doer.run(colId, docId, sPages,not(doNotBlockSeg),not(doNotLineSeg))
    traceln(jobid)
        
    traceln()      
    traceln("- Done")
    
