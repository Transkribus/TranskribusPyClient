#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""

    H. Déjean - Dec 2016


    Copyright Xerox(C) 2016 H. Déjean

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

"""
from __future__ import absolute_import
from __future__ import  print_function
from __future__ import unicode_literals
from io import open


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
from TranskribusPyClient.client import TranskribusClient
from TranskribusCommands.do_transcript import DoTranscript
from TranskribusPyClient.common.IntegerRange import IntegerRange
from TranskribusPyClient.TRP_FullDoc import TRP_FullDoc


from TranskribusPyClient.common.trace import traceln, trace

DEBUG = 0

description = """Apply Layout Analysis (LA) 

The syntax for specifying the page range is:
- one or several specifiers separated by a comma
- one separator is a page number, or a range of page number, e.g. 3-8
- Examples: 1   1,3,5   1-3    1,3,5-99,100

""" + _Trnskrbs_description

usage = """%s <colId> <docid/pagerange>
"""%sys.argv[0]

class DoLAbatch(TranskribusClient):
    """
            Hi Hervé,
        
        Sebastian has done the integration of the tools and can answer more indepth questions.
        
        Please take a look at:
        https://transkribus.eu/TrpServer/Swadl/wadl.html
        
        or
        
        https://transkribus.eu/TrpServer/rest/application.wadl
        
        The new methods are at:
        /LA/analyze
        
        Valid values for the jobImpl parameter are:
        NcsrLaJob
        CvlLaJob
        CITlabAdvancedLaJob
        
        You have to post a list of descriptor objects either as XML or JSON to the service, specifying the pages that have to be analyzed. A single page descriptor would look like this (regionId optional):
        <documentSelectionDescriptor>
            <docId>1</docId>
            <pageList>
                <pages>
                    <pageId>2</pageId>
                    <tsId>3</tsId>
                    <regionIds>aRegionId</regionIds>
                </pages>
            </pageList>
        </documentSelectionDescriptor>
        
        Do let us know if there are any problems with the new method.
        
        Best regards and have a nice weekend,
        Philip    
    
    
    13/12/2017:
        Hi Hervé,
        
        I just deployed the new LA job on the productive server, but the old
        behavior is still the default.
        
        If your client already can handle the /rest/LA/analyze call, all you
        have to do is append an additional query parameter to the POST request:
        
        ...&doCreateJobBatch=false
    
    
    """
    sDefaultServerUrl = _Trnskrbs_default_url
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
                
        self._trpMng = DoTranscript(self.sDefaultServerUrl, sHttpProxy=sHttpProxy, loggingLevel=loggingLevel)


    def jsonToXMLDescription(self,jsonDesc):
        """
            convert json description to XML


        <documentSelectionDescriptors>
             <documentSelectionDescriptor>
              <docId>1955</docId>
              <pageList>
               <pages>
                <pageId>9304</pageId>
                <tsId>22744</tsId>
               </pages>
              </pageList>
             </documentSelectionDescriptor>
            </documentSelectionDescriptors>
            
        """
#         import libxml2
#         s = '{"docId":17442,"pageList":{"pages":[{"pageId":400008,"tsId":1243509,"regionIds":[]}]}}'
#         s ='{"pageList": {"pages": [{"tsId": "1305027", "regionIds": [], "pageId": "478362"}]}, "docId": "18975"}'
# 
        jsonDesc=json.loads(jsonDesc)
    
        root = etree.Element("documentSelectionDescriptors")
        xmldesc= etree.ElementTree(root)
        
        root2 =etree.Element("documentSelectionDescriptor")
        root.append(root2)

        # docId
        node =  etree.Element("docId")
        root2.append(node)
        node.text = str(jsonDesc["docId"])
        
        #pageList
        nodelp = etree.Element("pageList")
        root2.append(nodelp)
                
        for page in jsonDesc["pageList"]['pages']:
            nodep = etree.Element("pages")
            nodelp.append(nodep)
            pageId = etree.Element("pageId")
            pageId.text = str(page['pageId'])
            tsId=etree.Element("tsId")
            tsId.text= str(page['tsId'])
            nodep.append(pageId)
            nodep.append(tsId)     
            # mandatory?
            if page['regionIds'] == []:
                regId=etree.Element("regionIds")
                regId.text = ''
                nodep.append(regId)
            else:
                for regid in (page['regionIds']):
                    regId=etree.Element("regionIds")
                    regId.text = str(regid)
                    nodep.append(regId)
            

        return etree.tostring(xmldesc, encoding='utf-8',pretty_print=True)    
#         return xmldesc.serialize('utf-8',True)    
            
    def buildDescription(self,colId,docpage,trp=None):
        """
            '{"docId":17442,"pageList":{"pages":[{"pageId":400008,"tsId":1243509,"regionIds":[]}]}}'
            or
            <documentSelectionDescriptor>
            <docId>1</docId>
            <pageList>
                <pages>
                    <pageId>2</pageId>
                    <tsId>3</tsId>
                    <regionIds>aRegionId</regionIds>
                </pages>
            </pageList>
        </documentSelectionDescriptor>            
            
        """
        jsonDesc = {}
        
        if trp is None:
            try: docId,pageRange= docpage.split('/')
            except ValueError: docId=docpage; pageRange = ""
            jsonDesc["docId"]=docId
            oPageRange = IntegerRange(pageRange)                 
            trpObj = self._trpMng.filter(colId,docId,page_filter=oPageRange,bLast=True)
        else:
            trpObj = TRP_FullDoc(trp)
        jsonDesc["pageList"]={}
#         pList= trpObj.getTranscriptList()
        jsonDesc["pageList"]['pages']= []
        for page in trpObj.getPageList():
            docId = page['docId']
            jsonDesc["docId"]=page['docId']
            jsonDesc["pageList"]['pages'].append({"pageId":page['pageId'],"tsId":page['tsList']['transcripts'][0]['tsId'],"regionIds":[]})
            #test for region 1949  319340/1 
#             jsonDesc["pageList"]['pages'].append({"pageId":page['pageId'],"tsId":page['tsList']['transcripts'][0]['tsId'],"regionIds":['region_1606307892218_46','region_1606308952428_122','region_1606309259629_175']})        
        return jsonDesc["docId"], json.dumps(jsonDesc)

    
    def run(self, colId, sDescription, sJobImpl,bBlockSeg=False,bCreateJobBatch=False):
        ret = self.analyzeLayoutNew(colId, sDescription,sJobImpl,"",bBlockSeg,bLineSeg=True,bCreateJobBatch=bCreateJobBatch)
        jobid= self.getJobIDsFromXMLStatuses(ret)
        return ret,jobid



def test_json2xml():
    
    s = '{"docId":17442,"pageList":{"pages":[{"pageId":400008,"tsId":1243509,"regionIds":[]}]}}'
    jsonDesc=json.loads(s)
    print(jsonDesc)
    
    root = etree.Element("documentSelectionDescriptors")
    xmldesc= etree.ElementTree(root)
        
    # docId
    node = etree.Element("docId")
    root.append(node)
    node.text = str(jsonDesc["docId"])
    
    #pageList
    nodelp = etree.Element("pageList")
    root.append(nodelp)
    nodep = etree.Element("pages")
    nodelp.append(nodep)
            
    for page in jsonDesc["pageList"]['pages']:
        pageId=etree.Element("pageId")
        pageId.text = str(page['pageId'])
        tsId=etree.Element("tsId")
        tsId.text = str(page['tsId'])
        regId=etree.Element("regionIds")
        regId.text =''
        nodep.append(pageId)
        nodep.append(tsId)
        nodep.append(regId)
    
    print(etree.tostring(xmldesc,pretty_print=True, encoding='utf-8'))    
    
    

if __name__ == '__main__':
    version = "v.01"
    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoLAbatch.sDefaultServerUrl)
        
    parser.add_option("--trp"  , dest='trp_doc', action="store", type="string",default=None, help="use trp doc file")
    parser.add_option("--doRegionSeg"  , dest='doRegionSeg'   , action="store_true",  default=False, help="do Region detection")        
    parser.add_option("--batchjob"  , dest='doBatchJob'   , action="store_true",  default=False, help="do one job per page")        

    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    doer = DoLAbatch(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    doer._trpMng.setSessionId(doer._sessionID)
    
    # --- 
    try:                        colId = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
    try:                        docidpages = args.pop(0)
    except Exception as e:      _exit(usage, 1, e)    
    if args:                    _exit(usage, 2, Exception("Extra arguments to the command"))

    # --- 
    # do the job...
    if options.trp_doc:
        trpdoc =  json.load(open(options.trp_doc, "r",encoding='utf-8'))
        docId,sPageDesc = doer.buildDescription(colId,docidpages,trpdoc)
    else:
        docId,sPageDesc = doer.buildDescription(colId,docidpages)
#     NcsrLaJob
#     CITlabAdvancedLaJob
    sPageDesc = doer.jsonToXMLDescription(sPageDesc)
    
    status, jobid = doer.run(colId, sPageDesc,'CITlabAdvancedLaJob',bBlockSeg=options.doRegionSeg,bCreateJobBatch=options.doBatchJob)
    traceln("job ID:",jobid)
    traceln("- Done")
    
