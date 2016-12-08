# -*- coding: utf-8 -*-

#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os
import logging

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusPyClient.test import _colId_A, _docId_a
from TranskribusPyClient.client import TranskribusClient, getStoredCredentials


login, pwd = getStoredCredentials()

conn = TranskribusClient(proxies={'https':'http://cornillon:8000'}
                         , loggingLevel=logging.INFO)
print conn

#print conn.auth_logout()

sessionID = conn.auth_login(login, pwd)
print sessionID

#sessionID = conn.auth_login("jean-luc.meunier@xrce.xerox.com", "trnjluc", sHttpsProxyUrl='http://cornillon:8000')



# ret = conn.getDocumentFromServer(colid, docid)
#ret = conn.getDocumentFromServer("3571", "7750")
data = conn.collections_fulldoc_xml(_colId_A, str(_docId_a))  #str just to stress-test
#data = conn.collections_fulldoc_xml(3571, "7750")
print data
"""

"""

conn.setProxies({'https':'http://cornillon:8000'})

print conn.auth_logout()

