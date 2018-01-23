# -*- coding: utf-8 -*-

#REMOVE THIS annoying warning saying:
#  /usr/lib/python2.7/site-packages/requests-2.12.1-py2.7.egg/requests/packages/urllib3/connectionpool.py:843: InsecureRequestWarning: Unverified HTTPS request is being made. 
#  Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings  InsecureRequestWarning)
from __future__ import absolute_import
from __future__ import  print_function
from __future__ import unicode_literals

import sys

import requests.packages.urllib3

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
DEBUG=0

_Trnskrbs_default_url = "https://transkribus.eu/TrpServer"

_Trnskrbs_description = u"""Pass your login/password as options otherwise consider having a Transkribus_credential.py file, which defines a 'login' and a 'pwd' variables.
 If you need to use a proxy, use the --https_proxy option or set the environment variables HTTPS_PROXY. 
 To use HTTP Basic Auth with your proxy, use the http://user:password@host/ syntax.
 """

sCOL = "col"
sMPXMLExtension = ".mpxml"

NS_PAGE_XML         = "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"

def __Trnskrbs_basic_options(parser, sDefaultServerUrl):
    """
    UTILITY
    add the usual options for Transkribus to a command line option parser
    """
    #prepare for the parsing of the command line
    #parser = OptionParser(usage=usage, version=version)
    
    parser.add_option("-s", "--server"  , dest='server', action="store", type="string", default=sDefaultServerUrl, help="Transkribus server URL")
    
    parser.add_option("-l", "--login"   , dest='login' , action="store", type="string", help="Transkribus login (consider storing your credentials in 'transkribus_credentials.py')")    
    parser.add_option("-p", "--pwd"     , dest='pwd'   , action="store", type="string", help="Transkribus password")

    parser.add_option("--persist"       , dest='persist', action="store_true", help="Try using an existing persistent session, or log-in and persists the session.")
    
    parser.add_option("--https_proxy"   , dest='https_proxy'  , action="store", type="string", help="proxy, e.g. http://cornillon:8000")


def __Trnskrbs_do_login_stuff(trnskrbs_client, options, trace=None, traceln=None):
    """
    deal with the complicated login variants...
        -trace and traceln are optional print methods 
    return True or raises an exception
    """  
    bOk = False
    
    if options.persist:
        #try getting some persistent session token
        if DEBUG and trace: trace("  ---login--- Try reusing persistent session ... ")
        try:
            bOk = trnskrbs_client.reusePersistentSession()
            if DEBUG and traceln: traceln("OK!")
        except:
            if DEBUG and traceln: traceln("Failed")
          
    if not bOk:
        if options.login:
            login, pwd = options.login, options.pwd
        else:
            if trace: DEBUG and trace("  ---login--- no login provided, looking for stored credentials... ")
            login, pwd = trnskrbs_client.getStoredCredentials(bAsk=False)
            if DEBUG and traceln: traceln("OK")    

        if DEBUG and traceln: trace("  ---login--- logging onto Transkribus as %s "%login)
        trnskrbs_client.auth_login(login, pwd)
        if DEBUG and traceln: traceln("OK")
        bOk = True

    return bOk

def _exit(usage, status, exc=None):
    if usage: sys.stderr.write("ERROR: usage : %s\n"%usage)
    if exc != None: sys.stderr.write(str(exc))  #any exception?
    sys.exit(status)    
    
    
def strTabularFormat(lDic, lsKey, sSortKey=None):
    """
    Format as a table a list of dictionary like:
        [
            {
                "modelName": "Marine_Lives",
                "nrOfTokens": 0,
                "isUsableInTranskribus": 1,
                "nrOfDictTokens": 0,
                "nrOfLines": 0,
                "modelId": 45
            },
         ...       
    Show only keys listed in lsKey
    if given, sSortKey is used to sort the lines of the table.
    return a string
    """
    if sSortKey: lDic.sort(key=lambda x: x[sSortKey])
    #computing column width
    lWidth = [1] * len(lsKey)
    for i, k in enumerate(lsKey): lWidth[i] = max(len(k), *[len(str(v[k])) for v in lDic])
    sFmt = "|".join(["%%(%s)%ds"%(name,k) for name, k in zip(lsKey, lWidth)])  #something like "%(modelName)25s %(modelId)13s ..."
    sFmt = sFmt + "\n"
    sRet = sFmt%{k:k for k in lsKey}    #table header
    sRet += sFmt % {s:("-"*n) for s,n in zip(lsKey, lWidth)}
    for record in lDic: sRet += sFmt % record
    return sRet
 