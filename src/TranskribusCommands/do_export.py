#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""

    Hervé Déjean - april 2021


    Copyright Naver LabsEurope (C) 2021 

    see https://transkribus.eu/wiki/index.php/HTR
"""
from __future__ import absolute_import
from __future__ import  print_function
from __future__ import unicode_literals

#    TranskribusCommands/do_htrTrainRnn model-name colId docid pages 


#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os, logging
from optparse import OptionParser
import json
from lxml import etree

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit
# from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit

from TranskribusPyClient.common.IntegerRange import IntegerRange
from TranskribusPyClient.common.trace import traceln, trace
from TranskribusPyClient.client import TranskribusClient


DEBUG = 0

description = """Export a document into alto format """


usage = """%s<colId> <docid> 
"""%sys.argv[0]

class Export(TranskribusClient):

    sDefaultServerUrl = _Trnskrbs_default_url
    params="""
{   "commonPars" : {
      "pages" : "1",
      "doExportDocMetadata" : true,
      "doWriteMets" : true,
      "doWriteImages" : true,
      "doExportPageXml" : true,
      "doExportAltoXml" : true,
      "doExportSingleTxtFiles" : false,
      "doWritePdf" : false,
      "doWriteTei" : false,
      "doWriteDocx" : false,
      "doWriteOneTxt" : false,
      "doWriteTagsXlsx" : false,
      "doWriteTagsIob" : false,
      "doWriteTablesXlsx" : false,
      "doWriteStructureInMets" : false,
      "doCreateTitle" : false,
      "useVersionStatus" : "Latest version",
      "writeTextOnWordLevel" : false,
      "doBlackening" : false,
      "selectedTags" : [ "add", "date", "Address", "human_production", "supplied", "work", "unclear", "sic", "structure", "div", "highlight", "place1", "regionType", "speech", "person", "gap", "organization", "comment", "abbrev", "place", "add1", "Initial", "lat" ],
      "font" : "FreeSerif",
      "splitIntoWordsInAltoXml" : true,
      "pageDirName" : "page",
      "fileNamePattern" : "${filename}",
      "useHttps" : true,
      "remoteImgQuality" : "orig",
      "doOverwrite" : true,
      "useOcrMasterDir" : true,
      "exportTranscriptMetadata" : true,
      "updatePageXmlImageDimensions" : false
   },
   "altoPars" : {
      "splitIntoWordsInAltoXml" : true
   },
   "pdfPars" : {
      "doPdfImagesOnly" : false,
      "doPdfImagesPlusText" : true,
      "doPdfWithTextPages" : false,
      "doPdfWithTags" : false,
      "doPdfWithArticles" : false,
      "doPdfA" : false,
      "pdfImgQuality" : "view"
   },
   "docxPars" : {
      "doDocxWithTags" : false,
      "doDocxPreserveLineBreaks" : false,
      "doDocxForcePageBreaks" : false,
      "doDocxMarkUnclear" : false,
      "doDocxKeepAbbrevs" : false,
      "doDocxExpandAbbrevs" : false,
      "doDocxSubstituteAbbrevs" : false,
      "doDocxWriteFilenames" : false,
      "doDocxIgnoreSuppliedTag" : false,
      "doDocxShowSuppliedTagWithBrackets" : false
   }
}
        """
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
    
    def run(self, colId, docid,sParams):
        ret = self.exportCollection(colId, docid,sParams)
        return ret
    

            
   
    
if __name__ == '__main__':
    version = "v.01"
    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, Export.sDefaultServerUrl)
        
    # parser.add_option("--trp"  , dest='trp_doc', action="store", type="string",default=None, help="use trp doc file")
    # parser.add_option("--templateID"  , dest='templateID'   , action="store", type="string" , help="template id")        
#     parser.add_option("--batchjob"  , dest='doBatchJob'   , action="store_true",  default=False, help="do one job per page")        

    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    doer = Export(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    # doer._trpMng.setSessionId(doer._sessionID)
    
    # --- 
    try:                        colId = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
    try:                        docid = args.pop(0)
    except Exception as e:      _exit(usage, 1, e)    
    if args:                    _exit(usage, 2, Exception("Extra arguments to the command"))

    # --- 

    jobid = doer.run(colId, docid,doer.params)
    traceln("job ID:",jobid)
    traceln("- Done")
    
