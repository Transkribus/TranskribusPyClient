#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    Utility to extract collection or documents from Transkribus and create DS test structures
    
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
    from the European Union�s Horizon 2020 research and innovation programme 
    under grant agreement No 674943.

Created on 15 Nov 2016

@author: meunier    
"""
DEBUG = 0

import sys, os, logging

from optparse import OptionParser
import glob

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from common.trace import traceln, trace

from TranskribusCommands import sCOL, sMPXMLExtension, _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit
from TranskribusPyClient.client import TranskribusClient

try:
    import xml_formats.PageXml as PageXml
except ImportError:
    sys.path.append( os.path.join( os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) ))))
                                    , "TranskribusDU", "src" ))
    import xml_formats.PageXml as PageXml
    
    


class TranskribusDownloader(TranskribusClient):
    """
    Download a Transkribus collection as a DS structured dataset
    """
    sDefaultServerUrl = _Trnskrbs_default_url
    
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=trnkbsServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
        

    def downloadCollection(self, colId, destDir, bForce=False, bNoImage=False):
        """
        Here, we create the appropriate structure and fetch either the whole collection or one document and convert this to DS XML

        if bForce==True, data on disk is overwritten, otherwise raise an exception is some data is there already
        if bNoImage==True, do not download the images
        """
        if not( os.path.exists(destDir) and os.path.isdir(destDir) ):
            raise ValueError("Non-existing destination folder"%destDir)
        
        colDir = os.path.join(destDir, "trnskrbs_%s"%colId)
            
        #Creating folder structure
        if os.path.exists(colDir): 
            if not os.path.isdir(colDir): raise ValueError("%s exists and is not a folder."%colDir)
        else:
            traceln('- creating folder: %s'%colDir)
            os.mkdir(colDir)

        for sSubDir in [sCOL, "xml", "ref", "run", "out"]:
            sDir = os.path.join(colDir, sSubDir)
            if os.path.exists(sDir):
                if not os.path.isdir(sDir): raise ValueError("%s exists and is not a folder."%sDir)
            else:
                os.mkdir(sDir)

        col_max_ts = self.download_collection(colId, os.path.join(colDir,sCOL), bForce, bNoImage)
        with open(destDir+os.sep+sCOL+TranskribusClient.POSTFIX_MAX_TX, "w") as fd: fd.write("%s"%col_max_ts) #"col_max.ts" file

        return col_max_ts, colDir
    
    def generateCollectionMultiPageXml(self, colDir, bStrict):
        """
        We concatenate all pages into a "multi-page PageXml" for each document of the collection
        return the list of XML filenames
        """
        lsXmlFilename = list()
        traceln("- Generating multi_page PageXml")
        lsDocMaxTSFilename = sorted(glob.iglob(os.path.join(colDir, "*%s"%TranskribusClient.POSTFIX_MAX_TX)), reverse=True)  # *_max.ts files
        for sDocMaxTSFilename in lsDocMaxTSFilename:
            
            docDir = sDocMaxTSFilename[:-len(TranskribusClient.POSTFIX_MAX_TX)]
            traceln("\t- %s"%docDir)
            
            doc = self.makeMultiPageXml(docDir)

            sXmlFilename = docDir+sMPXMLExtension
            self.writeDom(doc, sXmlFilename, True)
            lsXmlFilename.append(sXmlFilename)

            trace("\t\t- validating the MultiPageXml ...")
            if not PageXml.MultiPageXml.validate(doc): 
                if bStrict:
                    raise ValueError("Invalid XML generated in '%s'"%sXmlFilename)
                else:
                    traceln("   *** WARNING: XML file is invalid against the schema: '%s'"%sXmlFilename)
            traceln(" Ok!")
                
            if DEBUG>1:
                PageXml.MultiPageXml.splitMultiPageXml(doc, docDir, "debug_%d.xml", bIndent=True)
            
            doc.freeDoc()
            traceln('\t- %s'%sXmlFilename)

        
        return lsXmlFilename
            
    def makeMultiPageXml(self, docDir):
        """
        We concatenate all pages into a "multi-page PageXml"
        return a DOM
        """
        lsXmlDocFilename = sorted(glob.iglob(os.path.join(docDir, "*.pxml")), reverse=True)
        assert lsXmlDocFilename, "ERROR: a document should contain at least one XML file (extension .pxml): %s"%docDir
        
        doc = PageXml.MultiPageXml.makeMultiPageXml(lsXmlDocFilename)
        
        return doc
                
    def writeDom(self, doc, filename, bIndent=False):
        doc.saveFormatFileEnc(filename, "UTF-8", bIndent)
        
#         if self.bZLib:
#             #traceln("ZLIB WRITE")
#             try:
#                 FIX_docSetCompressMode(doc, self.iZLibRatio)
#             except Exception, e:
#                 traceln("WARNING: ZLib error in Component.py: cannot set the libxml2 in compression mode. Was libxml2 compiled with zlib? :", e)
#         if bIndent:
#             doc.saveFormatFileEnc(self.getOutputFileName(), "UTF-8",bIndent)
#         else: 
#             #JLM - April 2009 - dump does not support the compressiondoc.dump(self.getOutputFile())
#             doc.saveFileEnc(self.getOutputFileName(),"UTF-8")
     
if __name__ == '__main__':
    usage = "%s <colid> [<directory>]"%sys.argv[0]
    version = "v.02"
    description = "Extract a collection from transkribus and create a DS test structure containing that collection. \n" + _Trnskrbs_description

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, TranskribusDownloader.sDefaultServerUrl)
        
    parser.add_option("-f", "--force"   , dest='bForce' ,  action="store_true", default=False, help="Force rewrite if disk data is obsolete")    
    parser.add_option("--strict"        , dest='bStrict',  action="store_true", default=False, help="Failed schema validation stops the processus.")    
    parser.add_option("--noimage", "--noImage", dest='bNoImage', action="store_true", default=False, help="Do not download images.")    

    # --- 
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    try:
        colid = args.pop(0)
    except:
        _exit(usage, 1)

    if args:
        destDir = args[0]
    else:
        destDir = "."

    # --- 
    trnkbs2ds = TranskribusDownloader(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(trnkbs2ds, options, trace=trace, traceln=traceln)
    
    traceln("- Downloading collection %s to folder %s"%(colid, os.path.abspath(destDir)))
    col_ts, colDir = trnkbs2ds.downloadCollection(colid, destDir, bForce=options.bForce, bNoImage=options.bNoImage)
    traceln("- Done")
    
    with open(os.path.join(colDir, "config.txt"), "w") as fd: fd.write("server=%s\nforce=%s\nstrict=%s\n"%(options.server, options.bForce, options.bStrict))
    
    trnkbs2ds.generateCollectionMultiPageXml(os.path.join(colDir, sCOL), options.bStrict)
    
    traceln('- Done, see in %s'%colDir)
    
