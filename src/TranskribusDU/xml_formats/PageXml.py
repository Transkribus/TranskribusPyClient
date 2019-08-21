# -*- coding: utf-8 -*-

'''
Created on 21 Nov 2016


Various utilities to deal with PageXml format

@author: meunier
'''

from __future__ import absolute_import
from __future__ import  print_function
from __future__ import unicode_literals

import os
import datetime
from copy import deepcopy


from lxml import etree

class PageXmlException(Exception): pass


class PageXml:
    '''
    Various utilities to deal with PageXml format
    '''
    
    #Namespace for PageXml
    NS_PAGE_XML         = "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"
    
    NS_XSI ="http://www.w3.org/2001/XMLSchema-instance"
    XSILOCATION ="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15/pagecontent.xsd"  

    #Schema for Transkribus PageXml
    XSL_SCHEMA_FILENAME = "pagecontent.xsd"

    #XML schema loaded once for all
    cachedValidationContext = None  
    
    sMETADATA_ELT   = "Metadata"
    sCREATOR_ELT        = "Creator"
    sCREATED_ELT        = "Created"
    sLAST_CHANGE_ELT    = "LastChange"
    sCOMMENTS_ELT       = "Comments"
    sTranskribusMetadata_ELT = "TranskribusMetadata"
    sCUSTOM_ATTR = "custom"
    
    sEXT = ".pxml"

    # ---  Schema -------------------------------------            

    def validate(cls, doc):
        """
        Validate against the PageXml schema used by Transkribus
        
        Return True or False
        """
#         schDoc = cls.getSchemaAsDoc()
        if not cls.cachedValidationContext: 
            schemaFilename = cls.getSchemaFilename()
#             buff = open(schemaFilename).read()
            xmlschema_doc = etree.parse(schemaFilename)
            xmlschema = etree.XMLSchema(xmlschema_doc)            
            
#             prsrCtxt = libxml2.schemaNewMemParserCtxt(buff, len(buff))
#             schema = prsrCtxt.schemaParse()
#             cls.cachedValidationContext = schema.schemaNewValidCtxt()
            cls.cachedValidationContext = xmlschema
#             del buff , prsrCtxt

#         res = cls.cachedValidationContext.schemaValidateDoc(doc)
        bValid = cls.cachedValidationContext.validate(doc)
        log = cls.cachedValidationContext.error_log
        if not bValid: print(log)
        return bValid
         
    validate = classmethod(validate)

    def getSchemaFilename(cls):
        """
        Return the path to the schema, built from the path of this module.
        """
        filename = os.path.join(os.path.dirname(__file__), cls.XSL_SCHEMA_FILENAME)
        return filename
    getSchemaFilename = classmethod(getSchemaFilename)
    
    # ---  Metadata  -------------------------------------
    """
    <complexType name="MetadataType">
        <sequence>
            <element name="Creator" type="string"></element>
            <element name="Created" type="dateTime">
                <annotation>
                    <documentation>The timestamp has to be in UTC (Coordinated Universal Time) and not local time.</documentation></annotation></element>
            <element name="LastChange" type="dateTime">
                <annotation>
                    <documentation>The timestamp has to be in UTC (Coordinated Universal Time) and not local time.</documentation></annotation></element>
            <element name="Comments" type="string" minOccurs="0"
                maxOccurs="1"></element>
        </sequence>
    </complexType>
    """
    
    def getMetadata(cls, doc=None, domNd=None):
        """
        Parse the metadata of the PageXml DOM or of the given Metadata node
        return a Metadata object
        """
        _, ndCreator, ndCreated, ndLastChange, ndComments = cls._getMetadataNodes(doc, domNd)
        return Metadata(ndCreator.text
                        , ndCreated.text
                        , ndLastChange.text
                        , ndComments.text if ndComments is not None else None)
    getMetadata = classmethod(getMetadata)

    def setMetadata(cls, doc, domNd, Creator, Comments=None):
        """
        Pass EITHER a DOM or a Metadat DOM node!! (and pass None for the other)
        Set the metadata of the PageXml DOM or of the given Metadata node
        
        Update the Created and LastChange fields.
        Either update the Comments fields or delete it.
        
        You MUST indicate the Creator (a string)
        You MAY give a Comments (a string)
        The Created field is kept unchanged
        The LastChange field is automatically set.
        The Comments field is either updated or deleted.
        return the Metadata DOM node
        """
        ndMetadata, ndCreator, ndCreated, ndLastChange, ndComments = cls._getMetadataNodes(doc, domNd)
        ndCreator.text = Creator
        #The schema seems to call for GMT date&time  (IMU)
        #ISO 8601 says:  "If the time is in UTC, add a Z directly after the time without a space. Z is the zone designator for the zero UTC offset."
        #Python seems to break the standard unless one specifies properly a timezone by sub-classing tzinfo. But too complex stuff
        #So, I simply add a 'Z' 
        ndLastChange.text = datetime.datetime.utcnow().isoformat()+"Z" 
        if Comments != None:
            if not ndComments: #we need to add one!
                ndComments = etree.SubElement(ndMetadata, cls.sCOMMENTS_ELT)
            ndComments.text = Comments
        return ndMetadata
    setMetadata = classmethod(setMetadata)        
    
    # ---  Xml stuff -------------------------------------
    def getChildByName(cls, elt, sChildName):
        """
        look for all child elements having that name in PageXml namespace!!!
            Example: lNd = PageXMl.getChildByName(elt, "Baseline")
        return a DOM node
        """
        #return elt.findall(".//{%s}:%s"%(cls.NS_PAGE_XML,sChildName))
        return elt.xpath(".//pc:%s"%sChildName, namespaces={"pc":cls.NS_PAGE_XML})
#         ctxt = elt.doc.xpathNewContext()
#         ctxt.xpathRegisterNs("pc", cls.NS_PAGE_XML)  
#         ctxt.setContextNode(elt)
#         lNd = ctxt.xpathEval(".//pc:%s"%sChildName)
#         ctxt.xpathFreeContext()
#         return lNd
    getChildByName = classmethod(getChildByName)
    
    @classmethod
    def getAncestorByName(cls, elt, sName):
        return elt.xpath("ancestor::pc:%s"%sName, namespaces={"pc":cls.NS_PAGE_XML})
        
    
    def getCustomAttr(cls, nd, sAttrName, sSubAttrName=None):
        """
        Read the custom attribute, parse it, and extract the 1st or 1st and 2nd key value
        e.g. getCustomAttr(nd, "structure", "type")     -->  "catch-word"
        e.g. getCustomAttr(nd, "structure")             -->  {'type':'catch-word', "toto", "tutu"} 
        return a dictionary if no 2nd key provided, or a string if 1st and 2nd key provided
        Raise KeyError is one of the attribute does not exist
        """
        ddic = cls.parseCustomAttr( nd.get( cls.sCUSTOM_ATTR) )
        
        #First key
        try:
            dic2 = ddic[sAttrName]
            if sSubAttrName:
                return dic2[sSubAttrName]
            else:
                return dic2
        except KeyError as e:
            raise PageXmlException("node %s: %s and %s not found in %s"%(nd, sAttrName, sSubAttrName, ddic))
    getCustomAttr = classmethod(getCustomAttr)

    def setCustomAttr(cls, nd, sAttrName, sSubAttrName, sVal):
        """
        Change the custom attribute by setting the value of the 1st+2nd key in the DOM
        return the value
        Raise KeyError is one of the attribute does not exist
        """
        ddic = cls.parseCustomAttr( nd.get(cls.sCUSTOM_ATTR) )
        try:
            ddic[sAttrName][sSubAttrName] = str(sVal)
        except KeyError:
            ddic[sAttrName] = dict()
            ddic[sAttrName][sSubAttrName] = str(sVal)
            
        sddic = cls.formatCustomAttr(ddic)
        nd.set(cls.sCUSTOM_ATTR,sddic)
        return sVal
    setCustomAttr = classmethod(setCustomAttr)
    
    def parseCustomAttr(cls, s):
        """
        The custom attribute contains data in a CSS style syntax.
        We parse this syntax here and return a dictionary of dictionary
        
        Example:
        parseCustomAttr( "readingOrder {index:4;} structure {type:catch-word;}" )
            --> { 'readingOrder': { 'index':'4' }, 'structure':{'type':'catch-word'} }
        """
        dic = dict()
        
        s = s.strip()
        lChunk = s.split('}')
        if lChunk:
            for chunk in lChunk:    #things like  "a {x:1"
                chunk = chunk.strip()
                if not chunk: continue
                
                try:
                    sNames, sValues = chunk.split('{')   #things like: ("a,b", "x:1 ; y:2")
                except Exception:
                    raise ValueError("Expected a '{' in '%s'"%chunk)
                
                #the dictionary for that name
                dicValForName = dict()
                
                lsKeyVal = sValues.split(';') #things like  "x:1"
                for sKeyVal in lsKeyVal:
                    if not sKeyVal.strip(): continue  #empty
                    try:
                        sKey, sVal = sKeyVal.split(':')
                    except Exception:
                        raise ValueError("Expected a comma-separated string, got '%s'"%sKeyVal)
                    dicValForName[sKey.strip()] = sVal.strip()
                
                lName = sNames.split(',')
                for name in lName:
                    dic[name.strip()] = dicValForName
        return dic
    parseCustomAttr = classmethod(parseCustomAttr)
    
    def formatCustomAttr(cls, ddic):
        """
        Format a dictionary of dictionary of string in the "custom attribute" syntax 
        e.g. custom="readingOrder {index:1;} structure {type:heading;}"
        """
        s = ""
        for k1, d2 in ddic.items():
            if s: s += " "
            s += "%s"%k1
            s2 = ""
            for k2, v2 in d2.items():
                if s2: s2 += " "
                s2 += "%s:%s;"%(k2,v2)
            s += " {%s}"%s2
        return s
    formatCustomAttr = classmethod(formatCustomAttr)
        
        
    def makeText(cls, nd, ctxt=None):
        """
        build the text of a sub-tree by considering that textual nodes are tokens to be concatenated, with a space as separator
        NO! (JLM 2018)return None if no textual node found
        
        return empty string if no text node found
        """
        return " ".join(nd.itertext())
    makeText = classmethod(makeText)


    def addPrefix(cls, sPrefix, nd, sAttr="id"):
        """
        Utility to add a addPrefix to a certain attribute of a sub-tree.

        By default works on the 'id' attribute
                
        return the number of modified attributes
        """
        sAttr = sAttr.strip()
        lNd = nd.xpath(".//*[@%s]"%sAttr)
        ret = len(lNd)
        for nd in lNd:
            sNewValue = sPrefix+nd.get(sAttr)
            nd.set(sAttr,sNewValue)
#         ctxt.xpathFreeContext()   
        return ret
    addPrefix = classmethod(addPrefix)
                
    def rmPrefix(cls, sPrefix, nd, sAttr="id"):
        """
        Utility to remove a addPrefix from a certain attribute of a sub-tree.

        By default works on the 'id' attribute
                
        return the number of modified attributes        
        """
        sAttr = sAttr.strip()
#         ctxt = nd.doc.xpathNewContext()
#         ctxt.setContextNode(nd)
        lNd = nd.findall(".//*[@%s]"%sAttr)
        n = len(sPrefix)
        ret = len(lNd)
        for nd in lNd:
            sValue = nd.get(sAttr)
            assert sValue.startswith(sPrefix), "Prefix '%s' from attribute '@%s=%s' is missing"%(sPrefix, sAttr, sValue)
            sNewValue = sValue[n:]
            nd.set(sAttr,sNewValue)

#         ctxt.xpathFreeContext()   
        return ret
    rmPrefix = classmethod(rmPrefix)

    def _getMetadataNodes(cls, doc=None, domNd=None):
        """
        Parse the metadata of the PageXml DOM or of the given Metadata node
        return a 4-tuple:
            DOM nodes of Metadata, Creator, Created, Last_Change, Comments (or None if no COmments)
        """
        assert doc is None or domNd is None, "Internal error: pass either a DOM or a Metadata node"  #XOR
        if doc:
            lNd = cls.getChildByName(doc.getroot(), cls.sMETADATA_ELT)
            if len(lNd) != 1: raise ValueError("PageXml should have exactly one %s node"%cls.sMETADATA_ELT)
            domNd = lNd[0]
            assert etree.QName(domNd.tag).localname == cls.sMETADATA_ELT
#         nd1 = domNd.firstElementChild()
        nd1 = domNd[0]

        if etree.QName(nd1.tag).localname != cls.sCREATOR_ELT: raise ValueError("PageXMl mal-formed Metadata: Creator element must be 1st element")
        
        nd2 = nd1.getnext()
        if etree.QName(nd2.tag).localname != cls.sCREATED_ELT: raise ValueError("PageXMl mal-formed Metadata: Created element must be 2nd element")
        
        nd3 = nd2.getnext()
        if etree.QName(nd3.tag).localname != cls.sLAST_CHANGE_ELT: raise ValueError("PageXMl mal-formed Metadata: LastChange element must be 3rd element")
        
        nd4 = nd3.getnext()
        if nd4 is not None:
            if etree.QName(nd4.tag).localname not in [cls.sCOMMENTS_ELT,cls.sTranskribusMetadata_ELT] : raise ValueError("PageXMl mal-formed Metadata: LastChange element must be 3rd element")
        return domNd, nd1, nd2, nd3, nd4
    _getMetadataNodes = classmethod(_getMetadataNodes)

    # ---  Geometry -------------------------------------            
    def getPointList(cls, data):
        """
        get either an XML node of a PageXml object
              , or the content of a points attribute
        
        return the list of (x,y) of the polygone of the object - ( it is a list of int tuples)
        """
        try:
            lsPair = data.split(' ')
        except:
            lndPoints = data.xpath("(.//@points)[1]")
            sPoints = lndPoints[0] #.getContent()
            lsPair = sPoints.split(' ')
        lXY = list()
        for sPair in lsPair:
            (sx,sy) = sPair.split(',')
            lXY.append( (int(sx), int(sy)) )
        return lXY
    getPointList = classmethod(getPointList)


    def setPoints(cls, nd, lXY):
        """
        set the points attribute of that node to reflect the lXY values
        if nd is None, only returns the string that should be set to the @points attribute
        return the content of the @points attribute
        """
        sPairs = " ".join( ["%d,%d"%(int(x), int(y)) for x,y in lXY] )
        if nd is not None: nd.set("points", sPairs)
        return sPairs
    setPoints = classmethod(setPoints)

    def getPointsFromBB(cls, x1,y1,x2,y2):
        """
        get the polyline of this bounding box
        return a list of int tuples
        """
        return [ (x1,y1), (x2,y1), (x2,y2), (x1,y2), (x1,y1) ]
    getPointsFromBB = classmethod(getPointsFromBB)
        
        
        
    @classmethod
    # --- Creation -------------------------------------
    def createPageXmlDocument(cls,creatorName='NLE',filename=None,imgW=0, imgH=0):
        """
            create a new PageXml document
        """
        xmlPAGERoot = etree.Element('{%s}PcGts'%cls.NS_PAGE_XML,attrib={"{"+cls.NS_XSI+"}schemaLocation" : cls.XSILOCATION},nsmap={ None: cls.NS_PAGE_XML})
        xmlPageDoc = etree.ElementTree(xmlPAGERoot)

        metadata= etree.Element('{%s}%s'%(cls.NS_PAGE_XML,cls.sMETADATA_ELT))
        xmlPAGERoot.append(metadata)
        creator=etree.Element('{%s}%s'%(cls.NS_PAGE_XML,cls.sCREATOR_ELT))
        creator.text= creatorName
        created=etree.Element('{%s}%s'%(cls.NS_PAGE_XML,cls.sCREATED_ELT))
        created.text= datetime.datetime.now().isoformat()
        lastChange=etree.Element('{%s}%s'%(cls.NS_PAGE_XML,cls.sLAST_CHANGE_ELT))
        lastChange.text = datetime.datetime.utcnow().isoformat()+"Z" 
        metadata.append(creator)
        metadata.append(created)
        metadata.append(lastChange)
        
        
        pageNode= etree.Element('{%s}%s'%(cls.NS_PAGE_XML,'Page'))
#         pageNode.setNs(pagens)
        pageNode.set('imageFilename',filename )
        pageNode.set('imageWidth',str(imgW))
        pageNode.set('imageHeight',str(imgH))
    
        xmlPAGERoot.append(pageNode)
        
#         print (etree.tostring(xmlPageDoc))
        bValidate = cls.validate(xmlPageDoc)
        assert bValidate, 'new file not validated by schema'
        
        return xmlPageDoc, pageNode
    
    @classmethod
    def createPageXmlNode(cls,nodeName):
        """
            create a PageXMl element
        """
        node=etree.Element('{%s}%s'%(cls.NS_PAGE_XML,nodeName))
        
        return node
    
       
            
# ---  Multi-page PageXml -------------------------------------            
            
class MultiPageXml(PageXml):          
    XSL_SCHEMA_FILENAME = "multipagecontent.xsd"
    sEXT = ".mpxml"
    
    
    @classmethod
    def makeMultiPageXmlMemory(cls,lDom):
        """
            create a MultiPageXml from a list of dom PageXml
        """
        
        assert lDom, "ERROR: empty list of DOM PageXml"
        pnum = 1
        doc = lDom.pop(0)
        rootNd = doc.getroot()
        #Let's addPrefix all IDs with a page number...
        cls.addPrefix("p%d_"%pnum, rootNd, "id")
        
        while lDom:
            pnum += 1
            _doc = lDom.pop(0)
            _rootNd = _doc.getroot()
            assert etree.QName(_rootNd.tag).localname == "PcGts", "Data error: expected a root element named 'PcGts' in %d th dom" %pnum

            sPagePrefix = "p%d_"%pnum
            for ndChild in _rootNd:
#                 if ndChild.type == "element": 
                cls.addPrefix(sPagePrefix, ndChild, "id")
                rootNd.append(deepcopy(ndChild))  #1=recursive copy (properties, namespaces and children when applicable)
#                 ndChild = ndChild.next 
            
#             _doc.freeDoc()
        
        return doc
        
        
        
    def makeMultiPageXml(cls, lsXmlDocFilename):
        """
        We concatenate sequence of PageXml files into a multi-page (non-standard) PageXml
        
        Take a list of filenames,
        return a DOM
        """
        assert lsXmlDocFilename, "ERROR: empty list of filenames"
        
        pnum = 1
        sXmlFile = lsXmlDocFilename.pop(0)
        doc = etree.parse(sXmlFile)
        rootNd = doc.getroot()
        #Let's addPrefix all IDs with a page number...
        cls.addPrefix("p%d_"%pnum, rootNd, "id")
        
        while lsXmlDocFilename:
            pnum += 1
            sXmlFile = lsXmlDocFilename.pop(0)
            _doc = etree.parse(sXmlFile)
            _rootNd = _doc.getroot()
            assert etree.QName(_rootNd).localname == "PcGts", "Data error: expected a root element named 'PcGts' in %s"%sXmlFile

#             ndChild = _rootNd.children
            sPagePrefix = "p%d_"%pnum
            for ndChild in _rootNd:
#                 if ndChild.type == "element": 
                cls.addPrefix(sPagePrefix, ndChild, "id")
                rootNd.append(deepcopy(ndChild))   #.copyNode(1))  #1=recursive copy (properties, namespaces and children when applicable)
#                 ndChild = ndChild.next 
#             _doc.freeDoc()
        
        return doc
    makeMultiPageXml = classmethod(makeMultiPageXml)


    @classmethod
    def getNBPages(cls, doc):
        """
            return the number of pages of doc
        """
        return len(list(cls._iter_splitMultiPageXml(doc, bInPlace=False)))
        
    def splitMultiPageXml(cls, doc, sToDir, sFilenamePattern, bIndent=False, bInPlace=True):
        """
        Split a multipage PageXml into multiple PageXml files
        
        Take a folder name and a filename pattern containing a %d
        
        if bInPlace, the input doc is split in-place, to this function modifies the input doc, which must no longer be used by the caller.
        
        PROBLEM: 
            We have redundant declaration of the default namespace. 
            I don't know how to clean them, ax xmllint does with its --nsclean option.
        
        return a list of filenames
        """
        lXmlFilename = list()
        
        if not( os.path.exists(sToDir) and os.path.isdir(sToDir)): raise ValueError("%s is not a folder"%sToDir)
        
        for pnum, newDoc in cls._iter_splitMultiPageXml(doc, bInPlace):
            #dump the new XML into a file in target folder
            name = sFilenamePattern%pnum
            sFilename = os.path.join(sToDir, name)
#             newDoc.saveFormatFileEnc(sFilename, "UTF-8", bIndent)
            newDoc.write(sFilename, encoding="UTF-8", xml_declaration=True,pretty_print=True)

            lXmlFilename.append(sFilename)

        return lXmlFilename
    splitMultiPageXml = classmethod(splitMultiPageXml)

    # ---  Metadata  -------------------------------------
    def getMetadata(cls, doc=None, lDomNd=None):
        """
        Parse the metadata of the MultiPageXml DOM or of the given Metadata nodes
        return a list of Metadata object
        """
        lDomNd = cls._getMetadataNodeList(doc, lDomNd)
        return [PageXml.getMetadata(None, domNd) for domNd in lDomNd]
    getMetadata = classmethod(getMetadata)

    def setMetadata(cls, doc, lDomNd, Creator, Comments=None):
        """
        Pass EITHER a DOM or a Metadata DOM node list!! (and pass None for the other)
        Set the metadata of the PageXml DOM or of the given Metadata node
        
        Update the Created and LastChange fields.
        Either update the Comments fields or delete it.
        
        You MUST indicate the Creator (a string)
        You MAY give a Comments (a string)
        The Created field is kept unchanged
        The LastChange field is automatically set.
        The Comments field is either updated or deleted.
        return the Metadata DOM node
        """
        lDomNd = cls._getMetadataNodeList(doc, lDomNd)
        return [PageXml.setMetadata(None, domNd, Creator, Comments) for domNd in lDomNd]
    setMetadata = classmethod(setMetadata)        

    # ---  Internal  ------------------------------
    def _getMetadataNodeList(cls, doc=None, lDomNd=None):
        """
        Return the list of Metadata node
        return a non-empty list of DOM nodes 
        """
        assert bool(doc) != bool(lDomNd), "Internal error: pass either a DOM or a Metadata node list"  #XOR
        if doc:
            lDomNd = cls.getChildByName(doc.getroot(), cls.sMETADATA_ELT)
            if not lDomNd: raise ValueError("PageXml should have at least one %s node"%cls.sMETADATA_ELT)
        return lDomNd
    _getMetadataNodeList = classmethod(_getMetadataNodeList)
    
    def _iter_splitMultiPageXml(cls, doc, bInPlace=True):
        """
        iterator that splits a multipage PageXml into multiple PageXml DOM
        
        Take a MultiPageXMl DOM
        
        Yield a tupe (<pnum>, DOM)  for each PageXMl of each page. pnum is an integer in [1, ...]
        
        those DOMs are automatically freed at end of iteration
        
        if bInPlace, the input doc is split in-place, to this function modifies the input doc, which must no longer be used by the caller.
        
        PROBLEM: 
            We have redundant declaration of the default namespace. 
            I don't know how to clean them, ax xmllint does with its --nsclean option.
        
        yield DOMs
        """
        rootNd = doc.getroot()
        
#         ctxt = doc.xpathNewContext()
#         ctxt.xpathRegisterNs("a", cls.NS_PAGE_XML)
#         ctxt.setContextNode(rootNd)
        
#         lMetadataNd = ctxt.xpathEval("/a:PcGts/a:Metadata")
        lMetadataNd = rootNd.xpath("/x:PcGts/x:Metadata", namespaces={"x":cls.NS_PAGE_XML})
        if not lMetadataNd: raise ValueError("Input multi-page PageXml should have at least one page and therefore one Metadata element")
        
        lDocToBeFreed = []
        pnum = 0
        for metadataNd in lMetadataNd:
            pnum += 1
            
            #create a DOM
#             newRootNd = rootNd.copyNode(2) #2 copy properties and namespaces (when applicable)
            newRootNd = deepcopy(rootNd)   #2 copy properties and namespaces (when applicable)
            #newDoc = etree.ElementTree(newRootNd)
            xmlPAGERoot = etree.Element('{%s}PcGts'%cls.NS_PAGE_XML,attrib={"{"+cls.NS_XSI+"}schemaLocation" : cls.XSILOCATION},nsmap={ None: cls.NS_PAGE_XML})
            newDoc = etree.ElementTree(xmlPAGERoot)
    
            #to jump to the PAGE sibling node (we do it now, defore possibly unlink...)
            node = metadataNd.getnext()

#             #Add a copy of the METADATA node and sub-tree
            if bInPlace:
                metadataNd.getparent().remove(metadataNd)
                xmlPAGERoot.append(metadataNd)
            else:
                newMetadataNd=deepcopy(metadataNd)
                xmlPAGERoot.append(newMetadataNd)
            
#             #jump to the PAGE sibling node
#             node = metadataNd.next
            
            while node is not None:
#                 if node.type == "element": break
#                 node = node.next
                if node.tag != etree.Comment: break
                node = node.getnext()
            if etree.QName(node.tag).localname != "Page": raise ValueError("Input multi-page PageXml for page %d should have a PAGE node after the METADATA node."%pnum)
            #Add a copy of the PAGE node and sub-tree
            if bInPlace:
                xmlPAGERoot.append(node)
                newNode= node
            else:
                newNode = deepcopy(node)
                newRootNd.append(newNode)
            #Remove the prefix on the "id" attributes
            sPagePrefix = "p%d_"%pnum
            _ = cls.rmPrefix(sPagePrefix, newNode, "id")
            
            ###??? with lxml
#             newRootNd.reconciliateNs(newDoc)
            
            yield pnum, newDoc

            lDocToBeFreed.append(newDoc)
#             newDoc.freeDoc()
            
#         ctxt.xpathFreeContext()
#         for doc in lDocToBeFreed: doc.freeDoc()
           
        raise StopIteration
    _iter_splitMultiPageXml = classmethod(_iter_splitMultiPageXml)

# ---  Metadata of PageXml  --------------------------------            
class Metadata:
    
    """
    <complexType name="MetadataType">
        <sequence>
            <element name="Creator" type="string"></element>
            <element name="Created" type="dateTime">
                <annotation>
                    <documentation>The timestamp has to be in UTC (Coordinated Universal Time) and not local time.</documentation></annotation></element>
            <element name="LastChange" type="dateTime">
                <annotation>
                    <documentation>The timestamp has to be in UTC (Coordinated Universal Time) and not local time.</documentation></annotation></element>
            <element name="Comments" type="string" minOccurs="0"
                maxOccurs="1"></element>
        </sequence>
    </complexType>
    """
    
    def __init__(self, Creator, Created, LastChange, Comments=None):
        self.Creator    = Creator           # a string
        self.Created    = Created           # a string
        self.LastChange = LastChange        # a string
        self.Comments   = Comments          #None or a string
        
    
    
if __name__ == "__main__":
    
    import sys, glob, optparse
    usage = """
%s dirname+
Utility to create a set of MultipageXml XML files from a set of folders, each containing several PageXml files.
""" % sys.argv[0]

    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option("--format", dest='bIndent',  action="store_true"
                      , help="reformat/reindent the input")    
    parser.add_option("--compress", dest='bCompress',  action="store_true"
                      , help="Turn on gzip compression of output")    
    parser.add_option("--ext", dest='extension',  action="store", default=''
                      , help="process only .ext ")  
    (options, args) = parser.parse_args()

    try:
        lsDir = args
        lsDir[0]
    except:
        parser.print_help()
        parser.exit(1, "")
    
    print ("TODO: ", lsDir)
    
    for sDir in lsDir:
        if not os.path.isdir(sDir):
            print ("skipping %s (not a directory)"%sDir)
            continue
        
        print ("Processing %s..."%sDir,)
        if options.extension != '':
            l =      glob.glob(os.path.join(sDir, "*.%s"%options.extension))
        else:
            l =      glob.glob(os.path.join(sDir, "*.xml"))
            l.extend(glob.glob(os.path.join(sDir, "*.pxml")))
            l.extend(glob.glob(os.path.join(sDir, "*.xml.gz")))
            l.extend(glob.glob(os.path.join(sDir, "*.pxml.gz")))
        l.sort()
        print ("   %d pages"%len(l))
        
        doc = MultiPageXml.makeMultiPageXml(l)
        print(MultiPageXml.validate(doc))
        filename = sDir + ".mpxml"
        if options.bCompress:
            iCompress = 9
#             doc.setDocCompressMode(9)
        else:
            iCompress = 0
#             doc.setDocCompressMode(0)
        
        doc.write(filename,encoding='UTF-8',xml_declaration=True, compression=iCompress) 
#             doc.setDocCompressMode(0)
        
#         doc.saveFormatFileEnc(filename, "utf-8", bool(options.bIndent))
#         doc.freeDoc()
        del(doc)
        
        print ("\t done: %s"%filename)
        
    print ("DONE")
        