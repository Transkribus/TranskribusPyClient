#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""

    H Déjean


    Copyright NLE 2017 

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
from __future__ import unicode_literals


#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os, logging
import codecs

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

description = """upload a private dictionary

""" + _Trnskrbs_description

usage = """%s  <dictionary-name> -d <dictionary-file>

a single file called  <dictionary-name> will be created by concatenating   <dictionary-file> and will be uploaded in the tempDict user ftp folder
"""%sys.argv[0]

class DoHtrRnn(TranskribusClient):
    """
        Good morning,

        temp. dictionaries also can be sent now, see example below.
        The response will contain the dict. filename to be used in the HTR
        request's tempDict parameter. If extension of the given name does not
        match ".dict", this will be appended.
        The POST request's body should contain the dictionary data as UTF-8 String.
        The temp. dictionaries are now bound to the user account and you can
        check the transmission outcome by logging in via FTP to transkribus.eu
        with your credentials. There you will find a dir. called "dictTmp"
        containing the sent files, that will be used for HTR. You can also put
        dictionaries there via FTP and use them for HTR with the tempDict parameter.
        
        Best regards,
        Philip
        
        POST /TrpServerTesting/rest/recognition/tempDict?fileName=test.dict HTTP/1.1
        Host: transkribus.eu
        Content-Type: text/plain
        Cache-Control: no-cache
        
        er,124
...
    """
    sDefaultServerUrl = _Trnskrbs_default_url
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
        
    def run(self, dictName,dictString):
        ret = self.uploadDict(dictName,dictString)
        return ret

if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoHtrRnn.sDefaultServerUrl)
        
    parser.add_option("-d", "--dict"  , dest='ldict', action="append", type="string", help="list of dictionaries")
        
    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    doer = DoHtrRnn(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    # --- 
    try:                        dictName = args.pop(0)
    except Exception as e:      _exit(usage, 1, e)
#     try:                        filename = args.pop(0)
#     except Exception as e:      _exit(usage, 1, e)

    try:
        sfullDict="" 
        for filename in options.ldict:
            dictFile =codecs.open(filename,'r','utf-8').read()
            dictFile = dictFile.replace('\t',',')
            sfullDict += dictFile #+ '\n'
            traceln( "loaded %s"%(filename))
    except  IOError:print 'not possible to open file :%s'%(filename)
    
#     print sfullDict.encode("utf-8")
    # need to normalize the weights when build this different dictionaries???
    response  = doer.run(dictName, sfullDict)
    traceln(response)
        
    traceln()      
    traceln("- Done")
    
