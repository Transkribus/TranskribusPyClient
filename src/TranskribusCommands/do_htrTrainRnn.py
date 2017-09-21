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

#    TranskribusCommands/do_htrTrainRnn model-name colId docid pages 


#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os, logging
from optparse import OptionParser
from pygments.unistring import Ll
# import json

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit,\
    sCOL
from do_transcript import DoTranscript

from common.IntegerRange import IntegerRange
from TranskribusPyClient.TRP_FullDoc import TRP_FullDoc

from TranskribusPyClient.client import TranskribusClient
from common.trace import traceln, trace
import  codecs
import json
from random import shuffle


DEBUG = 0

description = """Train an HTR RNN model.

The syntax for specifying the page range is:
- one or several specifiers separated by a comma
- one separator is a page number, or a range of page number, e.g. 3-8
- Examples: 1   1,3,5   1-3    1,3,5-99,100
""" + _Trnskrbs_description

usage = """%s <model-name> <colId> 
"""%sys.argv[0]   

class DoHtrRnnTrain(TranskribusClient):
    sDefaultServerUrl = _Trnskrbs_default_url
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
    
        self._trpMng = DoTranscript(self.sDefaultServerUrl, sHttpProxy=sHttpProxy, loggingLevel=loggingLevel)
        
        self.percTest=0.1
        
        
    def run(self, sModelName,colID,lTrain, lTest, options,lcombinations):
        ljobid=[]
        for i,(lr, epochs,batch) in enumerate(lcombinations):
            sDesc = options.description  
            xmlconf =self.createXMLConf(sModelName, colID, lTrain, lTest, sDesc = sDesc, lang='German', numEpochs=epochs, learningRate=lr, noise='both', trainSizePerEpoch=batch)
            jobid = self.htrTrainingCITlab(xmlconf)
            ljobid.append(jobid)
            traceln("job id: %s"% jobid)
        return ljobid


    def createParamaterCombinations(self,learningrate,batchsize,epochs):
        """
            create a list of combinations of paramater
            one combination  -> one job
        """
        lLearningrate = learningrate.split(",")
        lEpochs = map(lambda x:int(x),epochs.split(","))
        lBatchsize = batchsize.split(",")
        
        return [( lr, epochs,batch ) for batch in lBatchsize for lr in lLearningrate for epochs in lEpochs]
        
    
    def createXMLConf(self,sModelName,colID,lTrain,lTest,sDesc='A description',lang='language shold be mentioned',numEpochs=200,learningRate=2e-3,noise='both',trainSizePerEpoch=1000):
        """
            create the XML configuration file
            see https://transkribus.eu/wiki/index.php/HTR

            
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <citLabHtrTrainConfig>
            <modelName>Test Model</modelName>
            <description>A description</description>
            <language>German</language>
            <colId>2</colId>
            <numEpochs>200</numEpochs>
            <learningRate>2e-3</learningRate>
            <noise>both</noise>
            <trainSizePerEpoch>1000</trainSizePerEpoch>
            <trainList>
                <train>
                    <docId>1</docId>
                    <pageList>
                        <pages>
                            <pageId>1</pageId>
                            <tsId>1</tsId>
                        </pages>
                        <pages>
                            <pageId>2</pageId>
                            <tsId>2</tsId>
                        </pages>
                    </pageList>
                </train>
                <train>
                    <docId>2</docId>
                    <pageList>
                        <pages>
                            <pageId>3</pageId>
                            <tsId>3</tsId>
                        </pages>
                        <pages>
                            <pageId>4</pageId>
                            <tsId>4</tsId>
                        </pages>
                    </pageList>
                </train>
            </trainList>
            <testList/>
        </citLabHtrTrainConfig>            
            
            
        """
#         print sModelName, colID, listDocID
        
        import libxml2
        confDoc= libxml2.newDoc("1.0")
        rootNode = libxml2.newNode("citLabHtrTrainConfig")
        confDoc.setRootElement(rootNode)
        node  = libxml2.newNode('modelName')
        node.setContent(sModelName)
        rootNode.addChild(node)
        node  = libxml2.newNode('description')
        node.setContent(sDesc)
        rootNode.addChild(node)
        node  = libxml2.newNode('language')
        node.setContent(lang)
        rootNode.addChild(node)
        node  = libxml2.newNode('colId')
        node.setContent("%s"%colID)
        rootNode.addChild(node)
        node  = libxml2.newNode('numEpochs')
        node.setContent('%s'%numEpochs)
        rootNode.addChild(node)
        node  = libxml2.newNode('learningRate')
        node.setContent('%s'%learningRate)
        rootNode.addChild(node)
        node  = libxml2.newNode('noise')
        node.setContent(noise)
        rootNode.addChild(node)
        node  = libxml2.newNode('trainSizePerEpoch')
        node.setContent('%s'%trainSizePerEpoch)
        rootNode.addChild(node)     
        
        trainListNode = libxml2.newNode('trainList')
        rootNode.addChild(trainListNode)
        testListNode = libxml2.newNode('testList')
        rootNode.addChild(testListNode)     
        for docid,pageid,tsid in lTrain:
            trainNode = libxml2.newNode('train')
            trainListNode.addChild(trainNode)
            docID= libxml2.newNode('docId')
            trainNode.addChild(docID)
            docID.setContent("%s"%docid)
            pageList= libxml2.newNode('pageList')
            trainNode.addChild(pageList)
#             for i in range(0,nbpages):
            pages= libxml2.newNode('pages')
            pageList.addChild(pages)
            pageId=libxml2.newNode('pageId')
            pageId.setContent('%s'%(pageid))
            pages.addChild(pageId)
            tsId=libxml2.newNode('tsId')
            tsId.setContent('%s'% (tsid))
            pages.addChild(tsId)      

        for docid,pageid,tsid in lTest:
            testNode = libxml2.newNode('test')
            testListNode.addChild(testNode)
            docID= libxml2.newNode('docId')
            testNode.addChild(docID)
            docID.setContent("%s"%docid)
            pageList= libxml2.newNode('pageList')
            testNode.addChild(pageList)
#             for i in range(0,nbpages):
            pages= libxml2.newNode('pages')
            pageList.addChild(pages)
            pageId=libxml2.newNode('pageId')
            pageId.setContent('%s'%(pageid))
            pages.addChild(pageId)
            tsId=libxml2.newNode('tsId')
            tsId.setContent('%s'% (tsid))
            pages.addChild(tsId) 
        
#         traceln('config:')
#         traceln(confDoc.serialize('utf-8',True))  
        return   confDoc.serialize('utf-8',True)        
    
    
    def createTrainTest(self,colId, ltrdoc,ltestdocId):
        """
            create train and test set
        
        pageList / pages /  pageNr /    tsList / transcripts[0] / tsId
        
        """

        lTrain=[]        
        for i,docpage in enumerate(ltrdoc):
            docId,pageRange= docpage.split('/')
#             trpFile = os.path.join(sColDir,sCOL,str(docId),'trp.json')
#             if not( os.path.exists(trpFile)):
#                 raise ValueError("Non-existing trp.json file %s" % trpFile)
#             with codecs.open(trpFile, "rb",'utf-8') as fd: jTrp = json.load(fd)
#             
            oPageRange = IntegerRange(pageRange) 
            trp = self._trpMng.filter(colId,docId,page_filter=oPageRange,bLast=True)
            for page in trp.getPageList():
                lTrain.append((docId,page['pageId'],page['tsList']['transcripts'][0]['tsId']))
#                 print page['pageId'], page['tsList']['transcripts'][0]['tsId']
#             
#             shuffle(lAlltsId)
#             lngTest=  int(round(len(lAlltsId) * self.percTest))
#             lngTrain = len(lAlltsId) - lngTest
        
        lTest=[]
        for i,docpage in enumerate(ltestdocId):
            docId,pageRange= docpage.split('/')
            lAlltsId=[]
            oPageRange = IntegerRange(pageRange) 
            trp = self._trpMng.filter(colId,docId,page_filter=oPageRange,bLast=True)
#             print trp.report_short()
            for page in trp.getPageList():
                lTest.append((docId,page['pageId'],page['tsList']['transcripts'][0]['tsId']))


        return lTrain, lTest
        
if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoHtrRnnTrain.sDefaultServerUrl)
        
    parser.add_option("--trdoc"  , dest='ltrdoc'   , action="append", type="string", default=None, help="document/pages  for TRAINING")
#     parser.add_option("--trpage"  , dest='ltrpagerange'   , action="append", type="string", default=None, help="page range")
    parser.add_option("--tsdoc"  , dest='ltsdoc'   , action="append", type="string", default=None, help="document/pages for TESTING")
#     parser.add_option("--tspage"  , dest='ltspagerange'   , action="append", type="string", default=None, help="page range")
    parser.add_option("--epoch"  , dest='epochs'   , action="store", type="string", default=200, help="nb epochs",metavar='N[,N]')
    parser.add_option("--lr"  , dest='learningrate'   , action="store", type="string", default="2e-3", help="learning rate", metavar='F[,F]')
    parser.add_option("--batch"  , dest='batchsize'   , action="store", type="string", default=1000, help="batch size",metavar='N[,NF]')
    parser.add_option("--description"  , dest='description' , action="store", type="string", default="no description", help="model description")

    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}
    # --- 
    #def createXMLConf(self,sModelName,colID,listDocID,sDesc=None,lang = None,numEpochs=200,learningRate=2e-3,noise='both',trainSizePerEpoch=1000):
    
    doer = DoHtrRnnTrain(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    doer._trpMng.setSessionId(doer._sessionID)
    
    try:                        sModelName = args.pop(0)
    except Exception as e:      _exit(usage, 1, e)
#     try:                        sColDir = args.pop(0)
#     except Exception as e:      _exit(usage, 1, e)    
    try:                        colId = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
#     try:                        docId   = int(args.pop(0))
#     except Exception as e:      _exit(usage, 1, e)
#     try:                        PagesTSID   = eval(args.pop(0))
#     except Exception as e:      _exit(usage, 1, e)
    try:                        sPages = args.pop(0)
    except Exception as e:      sPages = None
    if args:                    _exit(usage, 2, Exception("Extra arguments to the command"))

    
#     # --- 
#     # do the job...
    lTrain,lTest = doer.createTrainTest(colId,options.ltrdoc,options.ltsdoc)
    lcombinations = doer.createParamaterCombinations(options.learningrate,options.batchsize,options.epochs)
#     xmlconf = doer.createXMLConf(sModelName,colId,lTrain,lTest,sDesc = options.description, lang='German', learningRate=options.learningrate,numEpochs=options.epochs, trainSizePerEpoch=options.batchsize)
    ljobids = doer.run(sModelName,colId,lTrain,lTest,options,lcombinations)
# #     traceln(jobid)
        
    traceln()      
    traceln("- training launched with job ID: %s" % ljobids)
    
