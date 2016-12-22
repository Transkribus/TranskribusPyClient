# -*- coding: utf-8 -*-

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

sessionID = conn.auth_login(login, pwd)
data = conn.listDocsByCollectionId(_colId_A)
import pprint
pprint.pprint(data)

print conn.auth_logout()

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