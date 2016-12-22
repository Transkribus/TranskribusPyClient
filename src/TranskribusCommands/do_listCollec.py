#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    List the content of a collection

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
from TranskribusPyClient.client import TranskribusClient
from common.trace import traceln, trace

DEBUG = 0

description = """List the content of one or several Transkribus collection.
""" + _Trnskrbs_description

usage = """%s <colId>+ 
"""%sys.argv[0]

class DoListCollec(TranskribusClient):
    """
    List the content of a collection
    """
    sDefaultServerUrl = _Trnskrbs_default_url
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
        
    def run(self, colId):
        """

[{u'collectionList': {u'colList': [{u'colId': 3571,
                                    u'colName': u'READDU',
                                    u'description': u'created by herve.dejean@xrce.xerox.com'}]},
  u'createdFromTimestamp': 33175290,
  u'createdToTimestamp': 33175290,
  u'docId': 7749,
  u'fimgStoreColl': u'TrpDoc_DEA_7749',
  u'nrOfPages': 10,
  u'scriptType': u'HANDWRITTEN',
  u'status': 0,
  u'title': u'MM_1_001',
  u'uploadTimestamp': 1478161395893L,
  u'uploader': u'herve.dejean@xrce.xerox.com',
  u'uploaderId': 275},
 {u'collectionList': {u'colList': [{u'colId': 3571,
                                    u'colName': u'READDU',
                                    u'description': u'created by herve.dejean@xrce.xerox.com'}]},
  u'createdFromTimestamp': 0,
  u'createdToTimestamp': 0,
  u'docId': 7750,
  u'fimgStoreColl': u'TrpDoc_DEA_7750',
  u'nrOfPages': 10,
  u'scriptType': u'HANDWRITTEN',
  u'status': 0,
  u'title': u'MM_1_005',
  u'uploadTimestamp': 1478161451242L,
  u'uploader': u'herve.dejean@xrce.xerox.com',
  u'uploaderId': 275}]
  
  """        
        data = self.listCollection(colId)
        if data:
            _d = data[0][u'collectionList'][u'colList'][0]
            print "Collection: %s  (%s)"%(_d[u'colName'], _d[u'colId'])
            
            while data:
                dic = data.pop(0)
                print ">> (%s) #p=%d  '%s' by %s  (status=%s)" % (dic[u'docId'], dic[u'nrOfPages'], dic[u'title'], dic[u'uploader'], dic[u'status'])
        else:
            print ">> Collection is empty!"
        
        

if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoListCollec.sDefaultServerUrl)
        
    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    #source collection(s)
    try:
        lColId = [ int(arg) for arg in args ]
    except Exception as e:
        _exit(usage, 1, e)

    # --- 
    doer = DoListCollec(options.server, proxies, loggingLevel=logging.INFO)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)

    # --- 
    # do the job...
    for colId in lColId:
        try:
            doer.run(colId)
        except Exception as e:
            traceln()
            traceln("ERROR: could not list collection '%d' "%colId)
            _exit("", 1, e)
        
    traceln()      
    traceln("- Done for %d collection(s)"%len(lColId))
    
