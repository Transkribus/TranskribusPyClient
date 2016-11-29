# -*- coding: utf-8 -*-

#optional: useful if you want to choose the logging level to something else than logging.WARN
import logging

from read.TranskribusPyClient.test import _coldId_Sandbox, _docId_a
from read.TranskribusPyClient.client import TranskribusClient, getStoredCredentials

login, pwd = getStoredCredentials()

conn = TranskribusClient(proxies={'https':'http://cornillon:8000'}, loggingLevel=logging.INFO)
sessionID = conn.auth_login(login, pwd)

data = conn.collections_addDocToCollection(_coldId_Sandbox, _docId_a)
"""
True or Exception
"""

print conn.auth_logout()

