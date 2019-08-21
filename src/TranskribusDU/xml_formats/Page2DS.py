# -*- coding: utf-8 -*-
""" 
    H. Déjean

    cpy Xerox 2011
    
    Page 2 DS  (prima format to xerox format)
    http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15
    
"""

from __future__ import absolute_import
from __future__ import  print_function
from __future__ import unicode_literals

import sys, os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))))

# import  libxml2
from lxml import etree

import common.Component as Component
import config.ds_xml_def as ds_xml
from common.trace import traceln


class primaAnalysis(Component.Component):
    #DEFINE the version, usage and description of this particular component
    usage = "[-f N.N] "
    version = "v1.23"
    description = "description: PAGE XML 2 DS"
    usage = " [-f NN] [-l NN] [--tag=TAGNAME]  "
    version = "$Revision: 1.1 $"
        
    name="primaAnalysis"
    kPTTRN  = "pattern"
    kDPI = "dpi"
    kREF= 'ref'
    kREFTAG= 'reftag'   
    kDOCID= 'docid'    
    kRegion='noRegion'
    kCanLine= 'canonicalline' 
    def __init__(self):

        Component.Component.__init__(self, "pageXMLconverter", self.usage, self.version, self.description) 
        self.sPttrn     = None
        self.dpi = 300
        self.bRef = False
        self.lRefTag = ()
        self.bSkipRegion= False
        self.bCanonicalLine = False
        
        self.xmlns='http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'
        
        self.id=1
    def setParams(self, dParams):
        """
        Always call first the Component setParams
        Here, we set our internal attribute according to a possibly specified value (otherwise it stays at its default value)
        """
        Component.Component.setParams(self, dParams)
        if self.kPTTRN in  dParams  : self.sPttrn     = dParams[self.kPTTRN]
        if self.kDPI in  dParams    : self.dpi          = int(dParams[self.kDPI])
        if self.kREF in dParams     : self.bRef         = dParams[self.kREF]
        if self.kREFTAG in dParams  : self.lRefTag   = tuple(dParams[self.kREFTAG])
        if self.kDOCID in dParams   : self.sDocID   =dParams[self.kDOCID]
        if self.kRegion in dParams  : self.bSkipRegion   =dParams[self.kRegion]
        if self.kCanLine in dParams : self.bCanonicalLine   =dParams[self.kCanLine]



    def baselineCanon(self,sList):
        """
            build a line 
                w = baseline w
                h = fH points?
                
            if baseline not horizontal: what to do?  
        """
        fH= 15
        minx = 9e9
        miny = 9e9
        maxx = 0
        maxy = 0        
        lList = sList.split(',') 
        for x,y in  zip(lList[0::2],lList[1::2]):
            minx = min(minx,float(x))
            maxx = max(maxx,float(x))
            miny = min(miny,float(y))
            maxy = max(maxy,float(y))
        return [minx,miny-fH,fH,maxx-minx]
        
        
    def regionBoundingBox(self,sList):
        """
            points = (x,y)+ 
        """
        minx = 9e9
        miny = 9e9
        maxx = 0
        maxy = 0        
#         lList = sList.getContent().split(' ')
        lList = sList.split(' ')

        for x,y in [x.split(',') for x in lList]:
            minx = min(minx,float(x))
            maxx = max(maxx,float(x))
            miny = min(miny,float(y))
            maxy = max(maxy,float(y))
        return [minx,miny,maxy-miny,maxx-minx]
              
    def regionBoundingBox2010(self,lList):
        minx = 9e9
        miny = 9e9
        maxx = 0
        maxy = 0
        for elt in lList:
            if float(elt.get("x")) < minx: minx = float(elt.get("x"))
            if float(elt.get("y")) < miny: miny = float(elt.get("y"))
            if float(elt.get("x")) > maxx: maxx = float(elt.get("x"))
            if float(elt.get("y")) > maxy: maxy = float(elt.get("y"))            
        return [minx,miny,maxy-miny,maxx-minx]          
    
    
    def getBBPage(self,lList):

        minx = 9e9
        miny = 9e9
        maxh = 0
        maxw = 0        
        for reg in lList:
            [x,y,h,w] = reg
            if x < minx: minx = x
            if y < miny: miny = y
            if w + x > maxw: maxw = w + x
            if h + y > maxh: maxh = h + y
              
        return [minx,miny,maxh,maxw]
            
    
    
    def getPoints(self,curNode):
        """
            extract polylines, and convert into points(pdf)
        """
        lPoints = curNode.xpath("./x:Coords/@%s"%'points' ,namespaces={'x':self.xmlns})
        if lPoints!= []:
            #sp = lPoints[0].replace(' ',',')
            lP = lPoints[0].split(' ')
            if lP != []:
                scaledP=  [ list(map(lambda x: 72.0* float(x) / self.dpi , xy.split(','))) for xy in lP]
                scaledP = " ".join([ "%.2f,%.2f"% (x,y) for (x,y) in scaledP])
#                 scaledP = str(list(scaledP))[1:-1].replace(' ','')
                return scaledP
        else:
            return ""
    
    def getTextLineSubStructure(self,dsNode,curNode):
        """
            curNode: TextRegion or cell
                ->TextLine
                
                ->Word 
                    PlainText
        """
#         document = curNode.doc
#         xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19"
#         ctxt.xpathRegisterNs("a", self.xmlns)
#         xpath  = "./{%s}:%s" % (self.xmlns,"TextLine")
#         ctxt.setContextNode(curNode)
        lLines = curNode.xpath("./x:%s" % ("TextLine"),namespaces={'x':self.xmlns})
#         ctxt.xpathFreeContext()
        for line in lLines:
            node = etree.Element('TEXT')
            try:
                node.set('id',line.get('id'))
            except:
                node.set('id',str(self.id))
                self.id += 1
                
                
            dsNode.append(node)
            ## attributs
            for attr in ['type','custom', 'DU_row','DU_header','DU_col']:
                if line.get(attr):     
                    node.set(attr, line.get(attr))            
            
                                  
            sp = self.getPoints(line)
            # polylines
            node.set('points',sp)
            
            
            ## baseline
            ## add @baselintpoints 
            ##<Baseline points="373,814 700,805 1027,785 1354,804 1681,783 2339,780"/>
#             blnode = etree.Element('BASELINE')
            
#             ctxt = line.doc.xpathNewContext()
#             ctxt.xpathRegisterNs("a", self.xmlns)
#             ctxt.setContextNode(line)
#             scaledP=None
#             xpath  = "./a:Baseline/@%s" % ("points")
            lPoints = line.xpath("./x:Baseline/@%s"%'points',namespaces={'x':self.xmlns})
            if lPoints!= []:
#                 sp = lPoints[0].replace(' ',',')
                lP = lPoints[0].split(' ')
                if lP != []:
                    scaledP=  [ list(map(lambda x: 72.0* float(x) / self.dpi , xy.split(','))) for xy in lP]
                    scaledP = " ".join([ "%.2f,%.2f"% (x,y) for (x,y) in scaledP])
                    node.set('blpoints',scaledP)
                    dsNode.append(node)
#                 try:
#                     scaledP =  list(map(lambda x: 72.0* float(x) / self.dpi,sp.split(',')))
#                     scaledP = str(scaledP)[1:-1].replace(' ','')
#                     node.set('blpoints',scaledP)
#                     dsNode.append(node)
#                 except IndexError: 
#                     pass            
            # text
#             ctxt = line.doc.xpathNewContext()
#             ctxt.xpathRegisterNs("a", self.xmlns)
#             xpath  = "./a:TextEquiv/a:Unicode"
#             ctxt.setContextNode(line)
            txt =line.xpath("./x:TextEquiv/x:Unicode",namespaces={'x':self.xmlns})
            ## assume just one Unicode tag
            if txt != []:
                node.text = txt[0].text
            
            
            lPoints = line.xpath("./x:Coords/@%s" % ("points"),namespaces={'x':self.xmlns})
            if lPoints != [] and lPoints[0] !="":
                if self.bCanonicalLine and scaledP is not None:
                    [xp,yp,hp,wp] = self.baselineCanon(scaledP)
                else: 
                    [x,y,h,w] = self.regionBoundingBox(lPoints[0])                
                    xp,yp,hp,wp  = list(map(lambda x: 72.0* x / self.dpi,(x,y,h,w)))
                node.set(ds_xml.sX,str(xp))
                node.set(ds_xml.sY,str(yp))
                node.set(ds_xml.sHeight,str(hp))
                node.set(ds_xml.sWidth,str(wp))            
            node.set('font-size','20')

#             # if word
#             
#             ctxt = line.doc.xpathNewContext()
#             ctxt.xpathRegisterNs("a", self.xmlns)
#             xpath  = "./a:%s" % ("Word")
#             ctxt.setContextNode(line)
#             lWords= ctxt.xpathEval(xpath)
#             ctxt.xpathFreeContext()
#             print lWords
#             if lWords == []:
#                 # get TextEquiv
#                 ctxt = line.doc.xpathNewContext()
#                 ctxt.xpathRegisterNs("a", self.xmlns)
#                 xpath  = "./a:TextEquiv/a:Unicode"
#                 ctxt.setContextNode(line)
#                 ltxt = ctxt.xpathEval(xpath)
#                 ctxt.xpathFreeContext()
#                 if ltxt != []:
#                     node.setContent(ltxt[0].getContent())
#                     print "??",node
#                     lCWords= ltxt[0].getContent().split(' ')
#                     for word in lCWords:
#                         wnode= etree.Element('TOKEN')
#                         wnode.set('font-color','BLACK')
#                         wnode.set('font-size','8')
#                         wnode.setContent(word)     
#                         node.append(wnode)
#                
#                     
#             for word in lWords:
#                 wnode= etree.Element('TOKEN')
#                 wnode.set('font-color','BLACK')
#                 wnode.set('font-size','8')
#                 node.append(wnode)
#                 ctxt = curNode.doc.xpathNewContext()
#                 ctxt.xpathRegisterNs("a", self.xmlns)
#                 xpath  = ".//a:%s" % ("Points")
#                 ctxt.setContextNode(word)
#                 lPoints = ctxt.xpathEval(xpath)
#                 ctxt.xpathFreeContext()
#                 if lPoints != []:
#                     [x,y,h,w] = self.regionBoundingBox(lPoints[0])
#                     xp,yp,hp,wp  = map(lambda x: 72.0* x / self.dpi,(x,y,h,w)) 
#                     wnode.set(ds_xml.sX,str(xp))
#                     wnode.set(ds_xml.sY,str(yp))
#                     wnode.set(ds_xml.sHeight,str(hp))
#                     wnode.set(ds_xml.sWidth,str(wp))                            
#                     ctxt = word.doc.xpathNewContext()
#                     ctxt.xpathRegisterNs("a", self.xmlns)
#                     xpath  = './a:TextEquiv/a:PlainText/text()'
#                     ctxt.setContextNode(word)
#                     ltexts= ctxt.xpathEval(xpath)
#                     ctxt.xpathFreeContext()
#                     if ltexts:
#                         wnode.setContent(document.encodeEntitiesReentrant(ltexts[0].getContent()))
#                  
#             print "final:",node
             
    def mergeTextRegionandCell(self,table):
        """
            CVL LA tool create 
        """
    def getTable(self,tableNode):
        """
            generate a DS TABLE and cells   (row needed??)
            
            <TableCell row="0" col="8" rowSpan="1" colSpan="3" id="TableCell_1490730233599_310">
                <Coords points="3311,96 3311,257 3404,257 3524,257 3621,257 3621,96 3524,96 3404,96"/>
                <CornerPts>0 1 4 5</CornerPts>
            </TableCell>            
        """
        
        dstable= etree.Element(ds_xml.sTABLE)
#         document = tableNode.doc
#         ctxt = document.xpathNewContext()
#         ctxt.xpathRegisterNs("a", self.xmlns)
#         xpath  = "./a:%s" % ("TableCell")
#         ctxt.setContextNode(tableNode)
        lCells = tableNode.xpath("./a:%s" % ("TableCell"),namespaces={"a":self.xmlns})
        sp = self.getPoints(tableNode)
        dstable.set('points',sp)
        
        for cell in lCells:
            cellNode = etree.Element(ds_xml.sCELL)
            dstable.append(cellNode)
            ## need to get x, y, h, w
            cellNode.set("id", cell.get('id'))
            cellNode.set("row", cell.get('row'))
            cellNode.set("col", cell.get('col'))
            if cell.get('rowSpan'): cellNode.set("rowSpan", cell.get('rowSpan'))
            if cell.get('colSpan'): cellNode.set("colSpan", cell.get('colSpan'))
            sp= self.getPoints(cell)
            cellNode.set('points',sp)        
            # BB
#             ctxt = cell.doc.xpathNewContext()
#             ctxt.xpathRegisterNs("a", self.xmlns)
#             xpath  = "./a:Coords/@%s" % ("points")
#             ctxt.setContextNode(cell)
            lPoints = cell.xpath("./x:Coords/@%s" % ("points"),namespaces={'x':self.xmlns})
            if lPoints != []:
                [x,y,h,w] = self.regionBoundingBox(lPoints[0])
                xp,yp,hp,wp  = map(lambda x: 72.0* x / self.dpi,(x,y,h,w))
                cellNode.set(ds_xml.sX,str(xp))
                cellNode.set(ds_xml.sY,str(yp))
                cellNode.set(ds_xml.sHeight,str(hp))
                cellNode.set(ds_xml.sWidth,str(wp))                    
            
            
            self.getTextLineSubStructure(cellNode,cell)
            
        return dstable

    def copyEdge(self,child):
        """
            <Edge DU_type="HorizontalEdge" w="1.000000" points="230,756 61,761"/>
        """
        node = etree.Element('EDGE')
        node.set('src',child.get('src'))
        node.set('tgt',child.get('tgt'))
        node.set('type',child.get('type'))
        node.set('w',child.get('proba'))
        node.set('label',child.get('label'))
        lPoints = child.get('points')
        lP = lPoints.split(' ')
        if lP != []:
            scaledP=  [ list(map(lambda x: 72.0* float(x) / self.dpi , xy.split(','))) for xy in lP]
            scaledP = " ".join([ "%.2f,%.2f"% (x,y) for (x,y) in scaledP])
            node.set('points',scaledP)
        return node
    
    def createRegion(self,pnode):
        """
            create REGION
        """
        dsnode = etree.Element("REGION")
        if pnode.get('type'):
            dsnode.set('type',pnode.get('type') )
        if pnode.get('custom'):
            dsnode.set('custom',pnode.get('custom') )
#         dsnode.set('structure',pnode.get('structure') )
        sp = self.getPoints(pnode)
        dsnode.set('points',sp)
        try:
            dsnode.set('id',pnode.get('id'))
        except:
            dsnode.set('id',str(self.id))
            self.id += 1
        return dsnode
            
    def convertPage(self,ipage,dspage):
        for child in ipage:
            if child.tag != etree.Comment:
                if not self.bRef or (self.bRef and child.tag in self.lRefTag): 
#                     ctxt = ipage.doc.xpathNewContext()
#                     ctxt.xpathRegisterNs("a", self.xmlns)
#                     xpath  = "./a:Coords/@%s" % ("points")
#                     ctxt.setContextNode(child)
                    childname =etree.QName(child.tag).localname
#                     lPoints = child.xpath("./{%s}Coords/@%s" % (self.xmlns,"points"))
                    lPoints = child.xpath("./x:Coords/@points", namespaces={"x":self.xmlns})
                    if childname =="Edge":
                        node = self.copyEdge(child)       
                        dspage.append(node)             
                    if lPoints !=[]:
                        [x,y,h,w] = self.regionBoundingBox(lPoints[0])
                        xp,yp,hp,wp  = map(lambda x: 72.0* x / self.dpi,(x,y,h,w))
                        if childname == "TextRegion":
                            #get type
                            node = self.createRegion(child)
                            if not self.bRef:
                                if not self.bSkipRegion:
                                    self.getTextLineSubStructure(node,child)
                                else:
                                    # no region
                                    self.getTextLineSubStructure(dspage,child)
                        elif childname == "Cluster":
                            #get type
                            node = self.createRegion(child)
                            node.tag = 'Cluster'
                            if not self.bRef:
                                if not self.bSkipRegion:
                                    self.getTextLineSubStructure(node,child)
                                else:
                                    # no region
                                    self.getTextLineSubStructure(dspage,child)
                        elif childname =="ImageRegion":
                            node = etree.Element("IMAGE")
                        elif childname =="LineDrawingRegion":
                            node = etree.Element("IMAGE")
                        elif childname =="GraphicRegion":
                            node = etree.Element("IMAGE")
                        elif childname =="SeparatorRegion":
                            node = etree.Element("SeparatorRegion")
                            sp= self.getPoints(child)
                            # polylines
                            node.set('points',sp)                                         
                        elif childname =="TableRegion":
                            node = self.getTable(child)
                        elif childname =="FrameRegion":
                            node = etree.Element("FRAME")
                        elif childname =="ChartRegion":
                            node = etree.Element("FRAME")
                        elif childname =="MathsRegion":
                            node = etree.Element("MATH")
                        elif  childname =="PrintSpace":
                            node = etree.Element("typeArea")                                     
                        else:
                            node = etree.Element(etree.QName(child.tag).localname)
#                             node = etree.Element(child.localname)
                            #node = etree.Element("MISC")
                        ## ADD ROTATION INFO
                        if child.get("orientation"):
                            rotation = child.get("orientation")
                            if float(rotation) == 0:
                                node.set("rotation","0")
                            elif float(rotation) == -90:
                                node.set("rotation","1")
                            elif float(rotation) == 90:
                                node.set("rotation","2")
                            elif float(rotation) == 180:
                                node.set("rotation","3")           
                        node.set(ds_xml.sX,str(xp))
                        node.set(ds_xml.sY,str(yp))
                        node.set(ds_xml.sHeight,str(hp))
                        node.set(ds_xml.sWidth,str(wp))
                        try:
                            sp = self.getPoints(child)
                            node.set('points',sp)
                        except:pass
                        if not self.bSkipRegion:
                            dspage.append(node)
#                     elif child.tag =="TableRegion":
#                         node = self.getTable(child) 
#                         dspage.append(node)
        
        return dspage
    
    def convert2DS(self,mprimedoc,sDocID):
        """
            convert a MPXMLDom to DSDOM
        """ 
        dsroot = etree.Element(ds_xml.sDOCUMENT)
        dsdom = etree.ElementTree(dsroot)
                
        
#         ctxt = mprimedoc.xpathNewContext()
#         ctxt.xpathRegisterNs("a", self.xmlns)
#         xpath  = "//a:%s" % ("Page")
#         lPages = ctxt.xpathEval(xpath)
#         ctxt.xpathFreeContext()
        lPages = mprimedoc.findall(".//{%s}%s"%(self.xmlns,'Page'))
        for ipageNumber,ipage in enumerate(lPages):
            page = etree.Element(ds_xml.sPAGE)
            dsroot.append(page)            
            page.set(ds_xml.sPageNumber,str(ipageNumber+1))
            page.set("imageFilename",'..%scol%s%s%s'%(os.sep,os.sep,sDocID,os.sep)+ ipage.get("imageFilename"))
            imageWidth =  72 * (float(ipage.get("imageWidth"))  / self.dpi)
            imageHeight = 72 * (float(ipage.get("imageHeight")) / self.dpi)
            page.set("width",str(imageWidth))
            page.set("height",str(imageHeight))
            page.set("imageWidth",str(imageWidth))
            page.set("imageHeight",str(imageHeight))            
            self.convertPage(ipage, page)
                
        self.addTagProcessToMetadata(dsdom)                 
        return dsdom         
                 
    def run(self):
        
        dsroot = etree.Element(ds_xml.sDOCUMENT)
        dsdom = etree.ElementTree(dsroot)
        

        import glob
#         xmlns='http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'
#         xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19"
        ipageNumber = 1
        for pathname in sorted(glob.iglob(self.sPttrn)):
                #pathname = it.next()
                traceln(pathname)
                primedoc = self.loadDom(pathname)
#                 page = etree.Element(ds_xml.sPAGE)
#                 page.set(ds_xml.sPageNumber,str(ipageNumber))
#                 ipageNumber += 1
#                 dsroot.append(page)            
#                 ctxt = primedoc.xpathNewContext()
#                 ctxt.xpathRegisterNs("a", self.xmlns)
#                 xpath  = "//a:%s" % ("Page")
#                 lPages = ctxt.xpathEval(xpath)
#                 ctxt.xpathFreeContext()
                lPages = primedoc.getroot().findall(".//{%s}%s"%(self.xmlns,'Page'))
                for ipage in lPages:
                    page = etree.Element(ds_xml.sPAGE)
                    page.set(ds_xml.sPageNumber,str(ipageNumber))
                    ipageNumber += 1
                    dsroot.append(page)                       
                    page.set("imageFilename",'..%scol%s%s%s'%(os.sep,os.sep,self.sDocID,os.sep)+ ipage.get("imageFilename"))
                    imageWidth =  72 * (float(ipage.get("imageWidth"))  / self.dpi)
                    imageHeight = 72 * (float(ipage.get("imageHeight")) / self.dpi)
                    page.set("width",str(imageWidth))
                    page.set("height",str(imageHeight))
                    page.set("imageWidth",str(imageWidth))
                    page.set("imageHeight",str(imageHeight))                       
                    imgNode = etree.Element("IMAGE")
                    imgNode.set("href",ipage.get("imageFilename"))
                    imgNode.set("x","0")
                    imgNode.set("y","0")
                    imgNode.set("height",str(imageHeight))
                    imgNode.set("width",str(imageWidth))
                    page.append(imgNode)
                    self.convertPage(ipage, page)
#         except StopIteration, e:
#             traceln("=== done.")
        self.addTagProcessToMetadata(dsdom)
        return dsdom
                
if __name__ == "__main__":
    
    #command line
    traceln( "=============================================================================")
    
    cmp = primaAnalysis()

    #prepare for the parsing of the command line
    cmp.createCommandLineParser()
    cmp.add_option("", "--"+cmp.kPTTRN, dest=cmp.kPTTRN, action="store", type="string", help="REQUIRED **: File name pattern, e.g. /tmp/*/to?o*.xml"   , metavar="<pattern>")
    cmp.add_option("--dpi", dest="dpi", action="store",  help="image resolution")
    cmp.add_option("--ref", dest="ref", action="store_true", default=False, help="generate ref file")
    cmp.add_option("--reftag", dest="reftag", action="append",  help="generate ref file")
    cmp.add_option("--noregion", dest="noRegion", action="store_true",  help="skip REGION tags")
    cmp.add_option("--canonicalline", dest="canonicalline", action="store_true",default=False , help="create regular line rectangle from baseline")

    cmp.add_option("--"+cmp.kDOCID, dest=cmp.kDOCID, action="store", type='string', help="docId in col")
    
 
    #parse the command line
    dParams, args = cmp.parseCommandLine()
    
    #Now we are back to the normal programmatic mode, we set the componenet parameters
    cmp.setParams(dParams)
    doc = cmp.run()
    cmp.writeDom(doc, True)

