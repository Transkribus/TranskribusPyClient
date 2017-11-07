#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    Utility to upload to Transkribus from a DS test structure
    
    Copyright Naver Labs Europe(C) 2017  JL. Meunier

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
    from the European Union�s Horizon 2020 research and innovation programme 
    under grant agreement No 674943.

Created on 11 October 2017

@author: meunier    
"""
DEBUG = 0

import sys, os, logging
import glob
from optparse import OptionParser
import json, codecs

import libxml2

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from common.trace import traceln, trace, flush

from TranskribusCommands import NS_PAGE_XML, sCOL, sMPXMLExtension, _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit
from TranskribusPyClient.client import TranskribusClient

try:
    import xml_formats.PageXml as PageXml
except ImportError:
    sys.path.append( os.path.join( os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) ))))
                                    , "TranskribusDU", "src" ))
    import xml_formats.PageXml as PageXml


class TranskribusTranscriptUploader(TranskribusClient):
    """
    Upload transcripts from the disk or memory to Transkribus 
    """
    sDefaultServerUrl = _Trnskrbs_default_url
    
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=trnkbsServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
        
    def uploadCollectionTranscript(self, colid, sColDSDir, sNote="",sToolName="", iVerbose=0):
        """
        Upload the transcripts of all document in that collection into Transkribus
        return nothing
        """
        if iVerbose: 
            traceln("- Uploading all transcripts from folder %s to collection %s"%(sColDSDir, colid))

        trpFilename = os.path.join(sColDSDir, "trp.json")
        traceln(" - reading %s"%trpFilename)
        if not os.path.exists(trpFilename):
            raise Exception("File not found %s. \nData probably created in --trp mode, so upload must be done in --trp mode."%trpFilename)
        trp = json.load(codecs.open(trpFilename, "rb",'utf-8'))
        
        for docid in [d["docId"] for d in trp]:
            self.uploadDocumentTranscript(colid, docid, sColDSDir, sNote=sNote, sToolName=sToolName, iVerbose=iVerbose)
        
        if iVerbose: 
            traceln("  Done (collection %s)"%colid)
        return

    def uploadDocumentTranscript(self, colid, docid, sColDSDir, sNote="",sToolName="", iVerbose=0):
        """
        Upload the transcripts of all document in that collection into Transkribus
        return nothing
        """
        trpFilename = os.path.join(sColDSDir, str(docid), "trp.json")
        traceln(" - reading %s"%trpFilename)
        if not os.path.exists(trpFilename):
            raise Exception("File not found %s. \nData probably created in --trp mode, so upload must be done in --trp mode."%trpFilename)
        trp = json.load(codecs.open(trpFilename, "rb",'utf-8'))
        self.uploadDocumentTranscript_by_trp(colid, docid, trp, sColDSDir, sNote=sNote, sToolName=sToolName, iVerbose=iVerbose)
        return
    
    def uploadDocumentTranscript_by_trp(self, colid, docid, trp, sColDSDir, sNote="",sToolName="", iVerbose=0):
        """
        Upload the transcripts of one document in that collection into Transkribus, as specified by the TRP data
        return nothing
        """
        if iVerbose:
            traceln("- Uploading as listed in TRP, the transcript(s) of document %s from folder %s to collection %s "%(docid, sColDSDir, colid))

        if docid:
            if str(trp["md"]["docId"]) != str(docid):
                raise ValueError("Document ID does not match docId of TRP data.")
        else:
            docid = trp["md"]["docId"]  

        pageList = trp["pageList"]

        docDir = os.path.join(sColDSDir, str(docid))
                              
        if not os.path.exists(docDir): raise ValueError("Document directory not found: %s" % docDir)
        
        lFileList= []
        for page in pageList['pages']:
            pagenum= page['pageNr']
            logging.info("\t\t- page %s"%pagenum)
            
            imgFileName = page['imgFileName']
            base,_= os.path.splitext(imgFileName)
            lFileList.append(base)
            
            tsId = page['tsList']["transcripts"][0]['tsId']
            sBaseName, _ = os.path.splitext(imgFileName)
            xmlFilename = docDir + os.sep + sBaseName + ".pxml"
            logging.info("\t\t\t%s"%xmlFilename)
            traceln("page %5d: %s : %s"%(pagenum, tsId, xmlFilename))
            assert os.path.exists(xmlFilename)
            with open(xmlFilename, "rb") as fd: sXMlTranscript = fd.read()
            
            self.postPageTranscript(colid, docid, pagenum, sXMlTranscript, parentId=tsId, bEncoded=True, sNote=sNote, sToolName=sToolName)
            
        if iVerbose:
            traceln("   Done (collection %s, document %s as per TRP)"%(colid, docid))
            
        return lFileList

def main():        
    usage = "%s <directory> <coldId> [<docId>]"%sys.argv[0]
    version = "v.01"
    description = """Upload the transcript(s) from the DS structure to Transkribus, either of the collection or one of its document(s). 
The <directory> must have been created by transkribus_downloader.py and should contain the 'col' directory and a trp.json file for the collection, and one per document (the 'out', 'ref', 'run', 'xml' folders are not used).
The page transcript from the single page PageXml files are uploaded. (The multi-page xml file(s) are ignored))    
""" + _Trnskrbs_description

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, TranskribusTranscriptUploader.sDefaultServerUrl)
        
    parser.add_option("-q", "--quiet"  , dest='bQuiet',  action="store_true", default=False, help="Quiet mode")    
    parser.add_option("--trp"  ,  dest='trp'  , action="store", type="string", help="download the content specified by the trp file.")    
    parser.add_option("--toolname",  dest='tool'  , action="store", type="string", default="", help="Set the Toolname metadata in Transkribus.")    
    parser.add_option("--message",  dest='message', action="store", type="string", default="", help="Set the message metadata in Transkribus.")    

    # --- 
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    iVerbose = 0 if options.bQuiet else 2
    # --- 
    try:    sDSDir = args.pop(0)
    except: _exit(usage, 1)
    if not(sDSDir.endswith(sCOL) or sDSDir.endswith(sCOL+os.path.sep)): 
        sColDSDir = os.path.abspath(os.path.join(sDSDir, sCOL))
    else:
        sColDSDir = os.path.abspath(sDSDir)
    if not( os.path.exists(sColDSDir) and os.path.isdir(sColDSDir) ):
        raise ValueError("Non-existing folder: %s "%sColDSDir)
        
    try:    colid = args.pop(0)
    except: _exit(usage, 1)
    
    try:    docid = args.pop(0)
    except: docid = None
    
    # --- 
    doer = TranskribusTranscriptUploader(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    
    if options.trp:
        trp = json.load(codecs.open(options.trp, "rb",'utf-8'))
        traceln("- Uploading to collection %s, as specified by trp data"%(colid))
        if not docid:
            docid = trp["md"]["docId"]
            traceln(" read docId from TRP: docId = %s"%docid) 
            sToolname = options.tool if options.tool else "Transkribus_uploader (--trp)"
        lFileList = doer.uploadDocumentTranscript_by_trp(colid, docid, trp, sColDSDir
                                , sNote=options.message, sToolName=sToolname, iVerbose=iVerbose)
        #traceln(map(lambda x: x.encode('utf-8'), lFileList))
    else:
        if docid == None:
            sToolname = options.tool if options.tool else "Transkribus_uploader"
            doer.uploadCollectionTranscript(colid, sColDSDir
                                , sNote=options.message, sToolName=sToolname, iVerbose=iVerbose)

        else:
            sToolname = options.tool if options.tool else "Transkribus_uploader (docid)"
            doer.uploadDocumentTranscript(colid, docid, sColDSDir
                                , sNote=options.message, sToolName=sToolname, iVerbose=iVerbose)
        
    traceln('- DONE, all transcripts were uploaded. See in collection %s'%colid)
    
if __name__ == '__main__':
    main()