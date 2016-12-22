# TranskribusPyClient
A Pythonic API and some command line tools to access the Transkribus server via its REST API




Also see in [TranskribusPyClient/client.html](http://htmlpreview.github.com/?https://github.com/Transkribus/TranskribusPyClient/blob/master/src/TranskribusPyClient/client.html
)

Help on module client:

NAME
    client - Transkribus REST API for Python clients

FILE
    c:\local\meunier\git\transkribuspyclient\src\transkribuspyclient\client.py

DESCRIPTION
    WORK IN PROGRESS...
    
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

CLASSES
    TranskribusClient
    
    class TranskribusClient
     |  See web sites below for a detailed description of the server API:
     |  
     |  - https://transkribus.eu/wiki/index.php/REST_Interface
     |  - https://transkribus.eu/TrpServer/rest/application.wadl
     |  - https://github.com/Transkribus
     |  
     |  -- Query Parameters
     |  Most parameters can be passed as string.
     |  
     |  Transkribus specifies some of them as xs:int for instance. 
     |  In that case, you can pass an int or a string, since we format them using the pythoninc "%s".
     |  
     |      
     |  -- Proxies
     |  If you need to use a proxy, you can configure individual requests with the proxies argument to the login method:
     |  
     |  myproxies = {
     |    'http': 'http://10.10.1.10:3128',
     |    'https': 'http://10.10.1.10:1080',
     |  }
     |  
     |  clientObj.auth_login("_login_", "_pwd_", proxies=myproxies)
     |  
     |  You can also configure proxies by setting the environment variables HTTP_PROXY and HTTPS_PROXY.
     |  
     |  $ export HTTP_PROXY="http://10.10.1.10:3128"
     |  $ export HTTPS_PROXY="http://10.10.1.10:1080"
     |  
     |  To use HTTP Basic Auth with your proxy, use the http://user:password@host/ syntax:
     |  proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
     |  
     |  To give a proxy for a specific scheme and host, use the scheme://hostname form for the key. This will match for any request to the given scheme and exact hostname.
     |  
     |  proxies = {'http://10.20.1.128': 'http://10.10.1.10:5323'}
     |  Note that proxy URLs must include the scheme.
     |  
     |  Methods defined here:
     |  
     |  LA_batch(self, colId, docId, sPages, bBlockSeg, bLineSeq)
     |      apply Layout Analysis
     |      int colId, 
     |      int docId,
     |      String pages, 
     |      boolean doBlockSeg,
     |      boolean doLineSeg,
     |  
     |  __init__(self, sServerUrl='https://transkribus.eu/TrpServer', proxies={}, loggingLevel=30)
     |      #--- --- INIT --- -------------------------------------------------------------------------------------------------------------
     |  
     |  auth_login(self, sLogin, sPwd, bPersist=True)
     |      login to the server
     |      If bPersistent is True, the session token is persisted on disk. 
     |      Further calls from another process can be made without login by using reusePersistentSession method
     |      Return True or raise an exception
     |  
     |  auth_logout(self)
     |      Logout from the server, remove any persistent session token from disk
     |      Return True or raise an exception
     |  
     |  cleanPersistentSession(self)
     |      remove from disk any persistent session token. Idempotent (no exception if disk is already clean)
     |      return True or raises an exception
     |  
     |  collection_createCollection(self, sName)
     |      create a new collectin with given name.
     |      Return the collection unique identifier: colId   (as a string)
     |  
     |  collection_deleteCollection(self, colId)
     |      delete a collection
     |      Return True
     |  
     |  collection_deleteDocument(self, colId, docId)
     |      delete a document from a collection
     |      Return True
     |  
     |  collections_addDocToCollection(self, colId, docId)
     |      Add document docId to collection colId   (this is not a copy!!)
     |      
     |      Return True or raises an Exception
     |      
     |      NOTE the REST API does not return the new DocId... :-/
     |  
     |  collections_copyDocToCollection(self, colIdFrom, docId, colIdTo, name=None)
     |      Copy document docId from collection colIdFrom to collection colIdTo
     |      The document is renamed if a name is provided
     |      
     |      Return True or raises an Exception
     |  
     |  collections_fulldoc(self, colId, docId, nrOfTranscripts=None)
     |      Return the Transkribus data structure ( Pythonic data ) 
     |      or raise an exception
     |      
     |      nrOfTranscripts can be either -1 (all), 0 (no transcripts) or any positive max. value of transcripts you want to receive per page.
     |  
     |  collections_fulldoc_xml(self, colId, docId, nrOfTranscripts=None, bParse=True)
     |      Return the Transkribus data structure (either parsed as a DOM or as a serialized XML, , i.e. a unicode string)
     |      or raise an exception
     |      
     |      If you get a DOM, you need to free it afterward using the _xmlFreeDoc method.
     |      
     |      nrOfTranscripts can be either -1 (all), 0 (no transcripts) or any positive max. value of transcripts you want to receive per page.
     |  
     |  collections_list(self, colId, index=None, nValues=None, sortColumn=None, sortDirection=None)
     |      Return the Transkribus data structure (Pythonic data) 
     |      or raise an exception
     |      
     |      Undocumented parameters, sorry.
     |  
     |  collections_listEditDeclFeats(self, colId)
     |      Return the Transkribus data structure (XML as a DOM) 
     |      or raise an exception
     |      
     |      Caller must free the DOM using the _xmlFreeDoc method of this object.
     |  
     |  collections_postPageTranscript(self, colId, docId, pnum, sXMlTranscript, bOverwrite=None, sNote=None, parentId=None, bPnumIsPageId=None, bEncoded=False)
     |      Post a new transcript for a page
     |      sXmlTranscript is a Python Unicode string
     |      
     |      return a serialized XMl like:
     |          <?xml version="1.0" encoding="UTF-8" standalone="yes"?><trpTranscriptMetadata><tsId>424778</tsId><parentTsId>-1</parentTsId><key>IXQDKIMHCKSJAAVUZLWMIKRV</key><pageId>252384</pageId><docId>8255</docId><pageNr>1</pageNr><url>https://dbis-thure.uibk.ac.at/f/Get?id=IXQDKIMHCKSJAAVUZLWMIKRV</url><status>IN_PROGRESS</status><userName>jean-luc.meunier@xrce.xerox.com</userName><userId>3556</userId><timestamp>1481281786096</timestamp><md5Sum></md5Sum><nrOfRegions>4</nrOfRegions><nrOfTranscribedRegions>3</nrOfTranscribedRegions><nrOfWordsInRegions>131</nrOfWordsInRegions><nrOfLines>41</nrOfLines><nrOfTranscribedLines>40</nrOfTranscribedLines><nrOfWordsInLines>168</nrOfWordsInLines><nrOfWords>0</nrOfWords><nrOfTranscribedWords>0</nrOfTranscribedWords></trpTranscriptMetadata>
     |          
     |          <trpTranscriptMetadata>
     |              <tsId>424778</tsId>
     |              <parentTsId>-1</parentTsId>
     |              <key>IXQDKIMHCKSJAAVUZLWMIKRV</key>
     |              <pageId>252384</pageId>
     |              <docId>8255</docId>
     |              <pageNr>1</pageNr>
     |              <url>https://dbis-thure.uibk.ac.at/f/Get?id=IXQDKIMHCKSJAAVUZLWMIKRV</url>
     |              <status>IN_PROGRESS</status>
     |              <userName>jean-luc.meunier@xrce.xerox.com</userName>
     |              <userId>3556</userId>
     |              <timestamp>1481281786096</timestamp>
     |              <md5Sum/>
     |              <nrOfRegions>4</nrOfRegions>
     |              <nrOfTranscribedRegions>3</nrOfTranscribedRegions>
     |              <nrOfWordsInRegions>131</nrOfWordsInRegions>
     |              <nrOfLines>41</nrOfLines>
     |              <nrOfTranscribedLines>40</nrOfTranscribedLines>
     |              <nrOfWordsInLines>168</nrOfWordsInLines>
     |              <nrOfWords>0</nrOfWords>
     |              <nrOfTranscribedWords>0</nrOfTranscribedWords>
     |          </trpTranscriptMetadata>
     |  
     |  download_collection(self, colId, collDir, bForce=False, bNoImage=False)
     |      Convenience method, not provided directly by the Transkribus API.
     |      
     |      Lazy download of the colId collection into the collDir folder.
     |      Lazy, because it does not download a document that is not more recent than the one one disk. It uses page timestamp to decide.
     |      Both the XML and images are fetched from the server. 
     |      
     |      The destination folder is created if required.
     |      It also creates 1 sub-folder per document in the collection. 
     |      If the folder exists, raise an exception, unless bForce is True in which case, the folder is removed and recreated.
     |      
     |      Return the maximum timestamp over all pages of the collection.
     |  
     |  download_document(self, colId, docId, docDir, min_ts=None, bForce=False, bNoImage=False)
     |      Convenience method, not provided directly by the Transkribus API.
     |      
     |      Lazy download of the colId, docId document into the docDir folder.
     |      Lazy, because it does not download a document that is not more recent than the given timestamp. It uses page timestamp to decide.
     |      Both the XML and images are fetched from the server. 
     |      
     |      If the destination folder exists, raise an exception, unless bForce is True in which case, the folder is removed and recreated.
     |      
     |      Return the maximum timestamp over all pages of the document.
     |  
     |  getJobStatus(self, jobid)
     |      return the job status ( dictionary)
     |      keys are the strings:
     |          jobId, docId, pageNr, pages, type, state, success, description, userName, userId, createTime, startTime, endTime, jobData, resumable, jobImpl
     |      state values: "CREATED", "RUNNING", "FINISHED", "FAILED"
     |  
     |  getSessionId(self)
     |      return the current session ID or None if not logged in
     |  
     |  recognition_htrDecode(self, colId, sHtrModelName, docId, sPages)
     |      Do the HTR using the given model.
     |      - Maybe you can set sPages to None, or both docId and sPage to None ?? 
     |      
     |      Return the Transkribus server response (a job id)
     |      or raise an exception
     |  
     |  recognition_htrModels(self)
     |      List the HTR models
     |      Return a list of dictionaries, like:
     |                  [
     |              {
     |                  "modelName": "Marine_Lives",
     |                  "nrOfTokens": 0,
     |                  "isUsableInTranskribus": 1,
     |                  "nrOfDictTokens": 0,
     |                  "nrOfLines": 0,
     |                  "modelId": 45
     |              },
     |           ...       
     |      
     |      or raise an exception
     |  
     |  recognition_htrRnnDecode(self, colId, sHtrModelName, sDictName, docId, sPages)
     |      Do the HTR using the given RNN model and dictionary.
     |      - Maybe you can set sPages to None, or both docId and sPage to None ?? 
     |      
     |      Return the Transkribus server response (a job id)
     |      or raise an exception
     |  
     |  recognition_htrRnnDicts(self)
     |      List the HTR RNN dictionaries
     |      Return a textual list of dictionary names, one per line 
     |      or raise an exception
     |      
     |      Undocumented parameters, sorry.
     |  
     |  recognition_htrRnnModels(self)
     |      List the HTR RNN models
     |      Return a textual list of dictionary names, one per line 
     |      or raise an exception
     |  
     |  reusePersistentSession(self)
     |      reuse the session Id from the session file, if any
     |      raise an Exception if no session stored
     |      return True
     |  
     |  setPersistentSession(self)
     |      persist the session. 
     |      To be called after login!
     |      
     |      return True or raises an exception
     |  
     |  setProxies(self, proxies)
     |      Proxies
     |      If you need to use a proxy, you can configure individual requests with the proxies argument to the login method:
     |      
     |      myproxies = {
     |        'http': 'http://10.10.1.10:3128',
     |        'https': 'http://10.10.1.10:1080',
     |      }
     |      
     |      You can also configure proxies by setting the environment variables HTTP_PROXY and HTTPS_PROXY.
     |      
     |      $ export HTTP_PROXY="http://10.10.1.10:3128"
     |      $ export HTTPS_PROXY="http://10.10.1.10:1080"
     |      
     |      To use HTTP Basic Auth with your proxy, use the http://user:password@host/ syntax:
     |      proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
     |      
     |      To give a proxy for a specific scheme and host, use the scheme://hostname form for the key. This will match for any request to the given scheme and exact hostname.
     |      
     |      proxies = {'http://10.20.1.128': 'http://10.10.1.10:5323'}
     |      Note that proxy URLs must include the scheme.
     |      
     |      return True or raise an exception
     |  
     |  setSessionId(self, sessionId)
     |      set the session ID
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  getStoredCredentials(cls, bAsk=False) from __builtin__.classobj
     |      alias for module function

FUNCTIONS
    getStoredCredentials(bAsk=False)

DATA
    utf8 = 'utf-8'


