#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""

    Hervé Déjean - Jan  2017


    Copyright Xerox(C) 2016 

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

from TranskribusCommands import  __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit

from do_analyzeLayout import DoLAbatch
from TranskribusPyClient.common.IntegerRange import IntegerRange
from TranskribusPyClient.TRP_FullDoc import TRP_FullDoc
from TranskribusPyClient.common.trace import traceln, trace


DEBUG = 0

description = """Apply a table template to a list of pages

The syntax for specifying the page range is:
- one or several specifiers separated by a comma
- one separator is a page number, or a range of page number, e.g. 3-8
- Examples: 1   1,3,5   1-3    1,3,5-99,100
""" + _Trnskrbs_description


usage = """%s --templateID <> <colId> <docid/pagerange> 
"""%sys.argv[0]

class DoTableTemplate(DoLAbatch):

    
    def run(self, templateID, colId, sDescription, sJobImpl):
        ret = self.tableMatching(templateID, colId, sDescription,  sJobImpl)
        jobid= self.getJobIDsFromXMLStatuses(ret)
        return ret,jobid
    

    def jsonToXMLDescription(self,jsonDesc):
        """
            convert json description to XML

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<jobParameters>
     <docList>
         <docs>
             <docId>1</docId>
             <pageList>
                 <pages>
                     <pageId>2</pageId>
                     <tsId>3</tsId>
                 </pages>
             </pageList>
         </docs>
     </docList>
     <params>
         <entry>
             <key>templateId</key>
             <value>1543</value>
         </entry>
     </params>
</jobParameters>
            
        """
#         s = '{"docId":17442,"pageList":{"pages":[{"pageId":400008,"tsId":1243509,"regionIds":[]}]}}'
#         s ='{"pageList": {"pages": [{"tsId": "1305027", "regionIds": [], "pageId": "478362"}]}, "docId": "18975"}'
# 
        jsonDesc=json.loads(jsonDesc)
    
        root = etree.Element("jobParameters")
        xmldesc= etree.ElementTree(root)
        root2 = etree.Element("jobParameters")
        root.append(root2)
        
        docList =etree.Element("docList")
#         root2.append(docList)
        root.append(docList)
        
        docs= etree.Element("docs")
        docList.append(docs)

        # docId
        node =  etree.Element("docId")
        docs.append(node)
        node.text = str(jsonDesc["docId"])
        
        #pageList
        nodelp = etree.Element("pageList")
        docs.append(nodelp)
                
        for page in jsonDesc["pageList"]['pages']:
            nodep = etree.Element("pages")
            nodelp.append(nodep)
            pageId = etree.Element("pageId")
            pageId.text = str(page['pageId'])
            tsId=etree.Element("tsId")
            tsId.text= str(page['tsId'])
#             regId=etree.Element("regionIds")
#             regId.text = ''
            nodep.append(pageId)
            nodep.append(tsId)
#             nodep.append(regId)

        params= etree.Element('params')
        root.append(params)
        
        entry=etree.Element('entry')
        params.append(entry)
        
        key=etree.Element('key')
        key.text = 'templateId'
        entry.append(key)
  
        value=etree.Element('value')
        value.text= str(jsonDesc['template'])
        entry.append(value)

        return etree.tostring(xmldesc, encoding='utf-8',pretty_print=True)       
            
    def buildDescription(self,colId,docpage,templateId,trp=None):
        """
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <jobParameters>
     <docList>
         <docs>
             <docId>1</docId>
             <pageList>
                 <pages>
                     <pageId>2</pageId>
                     <tsId>3</tsId>
                 </pages>
             </pageList>
         </docs>
     </docList>
     <params>
         <entry>
             <key>templateId</key>
             <value>1543</value>
         </entry>
     </params>    
            
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
        jsonDesc['template'] = str(templateId)
        for page in trpObj.getPageList():
            docId = page['docId']
            jsonDesc["docId"]=page['docId']
            jsonDesc["pageList"]['pages'].append({"pageId":page['pageId'],"tsId":page['tsList']['transcripts'][0]['tsId'],"regionIds":[]})        
        
#         return jsonDesc["docId"], json.dumps(jsonDesc,encoding='utf-8')
        return jsonDesc["docId"], json.dumps(jsonDesc)    
    
if __name__ == '__main__':
    version = "v.01"
    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoTableTemplate.sDefaultServerUrl)
        
    parser.add_option("--trp"  , dest='trp_doc', action="store", type="string",default=None, help="use trp doc file")
    parser.add_option("--templateID"  , dest='templateID'   , action="store", type="string" , help="template id")        
#     parser.add_option("--batchjob"  , dest='doBatchJob'   , action="store_true",  default=False, help="do one job per page")        

    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    doer = DoTableTemplate(options.server, proxies, loggingLevel=logging.WARN)
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
        docId,sPageDesc = doer.buildDescription(colId,docidpages,options.templateID,trpdoc)
    else:
        docId,sPageDesc = doer.buildDescription(colId,docidpages,options.templateID)
#     NcsrLaJob
#     CITlabAdvancedLaJob
    sPageDesc = doer.jsonToXMLDescription(sPageDesc)
    """
        do_tableTemplate.py --temp 6078228 23017 87023/14
    """
    
    # jobImpl = CvlTableJob
    status, jobid = doer.run(options.templateID,colId, sPageDesc,"CvlTableJob")
    traceln("job ID:",jobid)
    traceln("- Done")
    
