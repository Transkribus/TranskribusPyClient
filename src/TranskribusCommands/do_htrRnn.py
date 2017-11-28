#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""

    JL Meunier - Dec 2016


    Copyright Xerox(C) 2016 JL. Meunier

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

#    TranskribusCommands/do_copyDocToCollec.py 3571 3820 8251 8252


#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os, logging
from optparse import OptionParser

import json
import codecs

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit
from TranskribusPyClient.client import TranskribusClient

from do_transcript import DoTranscript

from TranskribusPyClient.common.IntegerRange import IntegerRange
from TranskribusPyClient.TRP_FullDoc import TRP_FullDoc

from TranskribusPyClient.common.trace import traceln, trace

DEBUG = 0

description = """Apply an HTR RNN model.

The syntax for specifying the page range is:
- one or several specifiers separated by a comma
- one separator is a page number, or a range of page number, e.g. 3-8
- Examples: 1   1,3,5   1-3    1,3,5-99,100
""" + _Trnskrbs_description

usage = """%s <modelID> <dictionary-name> <colId> [--trp] [--docid]
"""%sys.argv[0]

class DoHtrRnn(TranskribusClient):
    """
        10/16/2017:  at region level
        {"docId":2278,"pageList":{"pages":[{"pageId":10070,"tsId":25143,"regionIds":["r2","r1"]}]}}
        
        Our client sends it like this:
        
        3 > POST
        https://transkribus.eu/TrpServerTesting/rest/recognition/2/241/htrCITlab?id=2278
        3 > Accept: text/plain
        ...
        3 > Content-Type: application/json
        3 > Cookie: $Version=1;JSESSIONID=....
        {"docId":2278,"pageList":{"pages":[{"pageId":10070,"tsId":25143,"regionIds":["r2","r1"]}]}}


    """
    sDefaultServerUrl = _Trnskrbs_default_url
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
        
        self._trpMng = DoTranscript(self.sDefaultServerUrl, sHttpProxy=sHttpProxy, loggingLevel=loggingLevel)

    def run(self, sModelID, sDictName, colId, docId, sDescPages,bDictTemp):
        ret = self.htrRnnDecode(colId, sModelID, sDictName, docId, sDescPages,bDictTemp)
        return ret

    def buildDescription(self,colId,docpage,trp=None):
        """
            '{"docId":17442,"pageList":{"pages":[{"pageId":400008,"tsId":1243509,"regionIds":[]}]}}'
        """
        jsonDesc = {}
        
        if trp is None:
            docId,pageRange= docpage.split('/')
            jsonDesc["docId"]=docId
            oPageRange = IntegerRange(pageRange)                 
            trpObj = self._trpMng.filter(colId,docId,page_filter=oPageRange,bLast=True)
        else:
            trpObj = TRP_FullDoc(trp)
        jsonDesc["pageList"]={}
#         pList= trpObj.getTranscriptList()
        jsonDesc["pageList"]['pages']= []
        for page in trpObj.getPageList():
            docId = page['docId']
            jsonDesc["docId"]=page['docId']
            jsonDesc["pageList"]['pages'].append({"pageId":page['pageId'],"tsId":page['tsList']['transcripts'][0]['tsId'],"regionIds":[]})        
        
        
        return jsonDesc["docId"], json.dumps(jsonDesc,encoding='utf-8')
    
if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoHtrRnn.sDefaultServerUrl)
        
    parser.add_option("-r", "--region"  , dest='region', action="store", type="string", default=DoHtrRnn.sDefaultServerUrl, help="apply HTR at region level")
    parser.add_option("--trp"  , dest='trp_doc', action="store", type="string",default=None, help="use trp doc file")
    parser.add_option("--docid"  , dest='docid'   , action="store", type="string", default=None, help="document/pages to be htr'd")
    parser.add_option("--tempdict"  , dest='dictTemp' , action="store_true", default=False, help="use tempDict folder")
# ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    doer = DoHtrRnn(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    doer._trpMng.setSessionId(doer._sessionID)

    # --- 
    
    try:                        sModelID = args.pop(0)
    except Exception as e:      _exit(usage, 1, e)
    try:                        sDictName = args.pop(0)
    except Exception as e:      _exit(usage, 1, e)
    try:                        colId = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
#     try:                        docId   = int(args.pop(0))
#     except Exception as e:      _exit(usage, 1, e)
#     try:                        sPages = args.pop(0)
#     except Exception as e:      sPages = None

    if args:                    _exit(usage, 2, Exception("Extra arguments to the command"))

    if options.trp_doc:
        trpdoc =  json.load(codecs.open(options.trp_doc, "rb",'utf-8'))
        docId,sPageDesc = doer.buildDescription(colId,options.docid,trpdoc)
    else:
        docId,sPageDesc = doer.buildDescription(colId,options.docid)

    # do the job...
    jobid = doer.run(sModelID, sDictName, colId, docId, sPageDesc,options.dictTemp)
    traceln(jobid)
        
    traceln()      
    traceln("- Done")
    
