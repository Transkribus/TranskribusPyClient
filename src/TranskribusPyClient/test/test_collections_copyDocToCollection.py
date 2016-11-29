# -*- coding: utf-8 -*-

#optional: useful if you want to choose the logging level to something else than logging.WARN
import logging

from read.TranskribusPyClient.test import _colId_A, _coldId_Sandbox, _docId_c, _docId_d
from read.TranskribusPyClient.client import TranskribusClient, getStoredCredentials

login, pwd = getStoredCredentials()

conn = TranskribusClient(proxies={'https':'http://cornillon:8000'}, loggingLevel=logging.INFO)
sessionID = conn.auth_login(login, pwd)

data = conn.collections_copyDocToCollection(_colId_A, _docId_c, _coldId_Sandbox, "named_by_JL")
data = conn.collections_copyDocToCollection(_colId_A, _docId_d, _coldId_Sandbox)
"""
True or Exception
"""

print conn.auth_logout()

