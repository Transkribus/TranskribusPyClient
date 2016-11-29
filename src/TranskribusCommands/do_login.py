#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    Utility to login into Transkribus and store the sessionId in a secure way for next commands

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

from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, _exit
from TranskribusPyClient.client import TranskribusClient, getStoredCredentials
from common.trace import traceln, trace

DEBUG = 0

description = """Login into Transkribus to avoid the need for login in next commands (until the session expires).
""" + _Trnskrbs_description

usage = """%s"""%sys.argv[0]

class DoLogin(TranskribusClient):
    """
    Download a Transkribus collection as a DS structured dataset
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
    __Trnskrbs_basic_options(parser, DoLogin.sDefaultServerUrl)
        
    #parse the command line
    (options, args) = parser.parse_args()

    # ---   
    #credentials and proxy
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    if options.login:
        login, pwd = options.login, options.pwd
    else:
        trace("- no login provided, looking for stored credentials... ")
        login, pwd = getStoredCredentials(bAsk=False)
        traceln("OK")

    # ------------------------------------------------------------------------------------------------
    
    doer = DoLogin(options.server, proxies, loggingLevel=logging.INFO)
    
    try:
        if options.persist:
            traceln("- Logging onto Transkribus as %s and making a persistent session"%login)
            doer.cleanPersistentSession()
            resp = doer.auth_login(login, pwd, bPersist=options.persist)
            traceln("\t --> %s"%os.path.join(DoLogin.sSESSION_FOLDER, DoLogin.sSESSION_FILENAME))
        else:
            trace("- Checking Transkribus login as %s "%login)
            resp = doer.auth_login(login, pwd, bPersist=options.persist)
            traceln(" OK!")
    except Exception as e:  _exit("", 1, e)
    
    traceln("- Done")

