# -*- coding: utf-8 -*-

#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os
import logging

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusPyClient.test import _coldId_Sandbox, _docId_a
from TranskribusPyClient.client import TranskribusClient, getStoredCredentials

login, pwd = getStoredCredentials()

conn = TranskribusClient(proxies={'https':'http://cornillon:8000'}, loggingLevel=logging.INFO)
sessionID = conn.auth_login(login, pwd)

data = conn.addDocToCollection(_coldId_Sandbox, _docId_a)
"""
True or Exception
"""

print conn.auth_logout()

