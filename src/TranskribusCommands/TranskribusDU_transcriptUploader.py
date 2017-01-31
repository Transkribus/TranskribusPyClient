#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    Utility to upload one or several transcripts of a document or collection to Transkribus
    
    Copyright Xerox(C) 2016  JL. Meunier

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

Created on 9 Dec 2016

@author: meunier    
"""
DEBUG = 0

import sys, os, logging
import glob
from optparse import OptionParser

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


sTRANSCRIPT_EXTENSION = "_du"+sMPXMLExtension   #e.g.   8551_du.mpxml

class TranskribusTranscriptUploader(TranskribusClient):
    """
    Upload transcripts from the disk or memory to Transkribus 
    """
    sDefaultServerUrl = _Trnskrbs_default_url
    
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=trnkbsServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
        
    def uploadCollectionTranscript(self, colid, sColDSDir, sTranscripExt=sTRANSCRIPT_EXTENSION, iVerbose=0):
        """
        Upload the transscripts of all document in that collection into Transkribus
        return nothing
        """
        if iVerbose: 
            traceln("- Uploading all transcripts from folder %s to collection %s"%(sColDSDir, colid))
        
        lsDocFilename = sorted(glob.iglob(os.path.join(sColDSDir, "*"+sTranscripExt)))
        for sDocFilename in lsDocFilename:
            sDocId = os.path.basename(sDocFilename)[:-len(sTranscripExt)]
            try:
                docid = int(sDocId)
            except ValueError:
                traceln("Warning: folder %s : %s invalid docid, IGNORING IT"%(sColDSDir, sDocId))
                continue
            self.uploadDocumentTranscript(colid, docid, sColDSDir, sTranscripExt=sTranscripExt, iVerbose=iVerbose)
        
        if iVerbose: 
            traceln("  Done (collection %s)"%colid)
        return

    def uploadDocumentTranscript(self, colid, docid, sColDSDir, sNote=None,sTranscripExt=sTRANSCRIPT_EXTENSION, iVerbose=0):
        """
        Upload the transscripts of all document in that collection into Transkribus
        return nothing
        """
        if iVerbose:
            traceln("- Uploading transcript of document %s from folder %s to collection %s "%(docid, sColDSDir, colid))

        sDocFilename = os.path.join(sColDSDir, str(docid)+sTranscripExt)
        doc = libxml2.parseFile(sDocFilename)

        if iVerbose > 1: traceln("\t%6s %s"%(docid, sDocFilename))
        for pnum, pageDoc in PageXml.MultiPageXml._iter_splitMultiPageXml(doc, bInPlace=True):
            #dump the new XML into a file in target folder
            if iVerbose > 1:
                if pnum%10 == 0: trace(" %d "%pnum) 
                else: trace(".")
                flush()
            sXMlTranscript = pageDoc.serialize("utf-8", True)
            self.postPageTranscript(colid, docid, pnum,sNote, sXMlTranscript, bEncoded=True)
        if iVerbose > 1: traceln("")
        
        doc.freeDoc()
        
        if iVerbose:
            traceln("   Done (collection %s, document %s)"%(colid, docid))
        return

        
if __name__ == '__main__':
    usage = "%s <directory> <coldId> [<docId>]"%sys.argv[0]
    version = "v.01"
    description = """Upload the DU transcript(s) from the DS structure to Transkribus, either of all or one of its %s file(s) to the given collection. 
The <directory> is the usual DS one and should contain the 'col' directory (the 'out', 'ref', 'run', 'xml' are not used).
Extract the page transcript from the MultiPageXml (not from the single page PageXml files!)    
"""%sTRANSCRIPT_EXTENSION + _Trnskrbs_description

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, TranskribusTranscriptUploader.sDefaultServerUrl)
        
    parser.add_option("--strict", dest='bStrict',  action="store_true", default=False, help="Failed schema validation stops the processus.")    
    parser.add_option("--nodu"  , dest='bNoDU',  action="store_true", default=False, help="Upload the non-DU transcript (the .mpxml one)")    
    parser.add_option("-q", "--quiet"  , dest='bQuiet',  action="store_true", default=False, help="Quiet mode")    

    # --- 
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    if options.bNoDU:
        sTRANSCRIPT_EXTENSION = sMPXMLExtension
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
    traceln("- Transcript will be taken from %s file(s) from: %s"%(sTRANSCRIPT_EXTENSION, sColDSDir))    
        
    try:    colid = args.pop(0)
    except: _exit(usage, 1)
    
    try:    docid = args.pop(0)
    except: docid = None
    
    # --- 
    doer = TranskribusTranscriptUploader(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    
    if docid == None:
        doer.uploadCollectionTranscript(colid, sColDSDir, sTranscripExt=sTRANSCRIPT_EXTENSION, iVerbose=iVerbose)
    else:
        doer.uploadDocumentTranscript(colid, docid, sColDSDir, sTranscripExt=sTRANSCRIPT_EXTENSION, iVerbose=iVerbose)
        
    
    traceln('- DONE, all transcripts were uploaded. See in collection %s'%colid)
    
