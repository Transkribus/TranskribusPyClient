#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    List the HTR RNN Models and Dictionaries

    JL Meunier - Dec 2016


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
# import json

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit, strTabularFormat
from TranskribusPyClient.client import TranskribusClient
from TranskribusPyClient.common.trace import traceln, trace

DEBUG = 0

description = """List HTR RNN models and dictionaries available in Transkribus.
""" + _Trnskrbs_description

usage = """%s
"""%sys.argv[0]

class DoListHtrRnn(TranskribusClient):
    sDefaultServerUrl = _Trnskrbs_default_url
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
    
    def run(self,colid=None,bListDict=False):
        """
        2 textual lists
        """
        sModels=None
        sColModels=None
        sDicts = None
        if colid is not None:
            sColModels = self.listRnns(colid)
            for models in sColModels:
                #some old? models do not have params field
                try: traceln("%s\t%s\t%s\ndescription:%s" % (models['htrId'],models['name'].strip(),models['params'].strip(),models['description'].strip()))
                except KeyError: traceln("%s\t%s\tno params" % (models['htrId'],models['name']))             
                traceln()
        else:
            sModels = self.listRnnsText()        
            traceln("\n--- Models ---------------------------")
            traceln(sModels)
        
        if bListDict:
            sDicts = self.listDictsText()        
            traceln("\n--- Dictionaries ---------------------")
            traceln(sDicts)
        
        return sModels, sColModels, sDicts

if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    parser.add_option("--colid", dest='colid', type='string', default=None, help = 'get models linked to the colid')
    parser.add_option("--dict", dest='dict', action='store_true', default=False, help = 'get dictionaries')

    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoListHtrRnn.sDefaultServerUrl)
        
    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}
    # --- 
    doer = DoListHtrRnn(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)

    # --- 
    # do the job...
    doer.run(options.colid,options.dict)
        
    traceln()      
    traceln("- Done")
    
