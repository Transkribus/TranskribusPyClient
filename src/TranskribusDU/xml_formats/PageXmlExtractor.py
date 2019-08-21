# -*- coding: utf-8 -*-

'''
Created on August 1st, 2017


Utility to extract several pages from several document to a folder or a MultiPageXml file

@author: meunier
'''

from __future__ import absolute_import
from __future__ import  print_function
from __future__ import unicode_literals

import os
from io import open
import json
import shutil
import math

import xml_formats.PageXml as PageXml

class DocPageSet:
    '''
    the list of pages of interest of a document
    take the textual form: docID=<page-range-set>]
        a page-range-set takes the form: <pageRange>[,<pageRange>]+
         with pageRange taking the form: N|N-N
        For instance: 111=1 or 222=1-10 or 333=1,10-20,3,40-50
        
    NOTE: ranges should not overlap!!! 
    '''
    def __init__(self, sSpec):
        try:
            sDocID, sPageRangeSet = sSpec.strip().split('=')
        except ValueError:
            raise ValueError("Malformed range: '%s'"%sSpec)
        
        self.sDocID = sDocID
        self._ltiRange = []
        prev_b = None
        for sPageRange in sPageRangeSet.split(","):
            lsN = sPageRange.split('-')
            if len(lsN) == 1:
                a = int(lsN[0])
                b = a
            elif len(lsN) == 2:
                a,b = int(lsN[0]), int(lsN[1])
            else:
                raise ValueError("invalid range: '%s'"%sPageRange)
            if not(a<=b): raise ValueError("Invalid range: '%s'"%sPageRange)
            self._ltiRange.append( (a,b) )     #222=1-10
            if prev_b < a:
                prev_b = b
            else:
                raise ValueError("unordered or overlapping ranges: '%d' >= '%d' '%s'"%(prev_b, a, sSpec))
        if not self.sDocID:   raise ValueError("missing docID: '%s'"%sSpec)
        if not self._ltiRange: raise ValueError("empty range: '%s'"%sSpec)
    
    # -----    
    def getDocID(self, bSkipPath=False):
        if bSkipPath:
            return os.path.basename(self.sDocID)
        else:
            return self.sDocID
    
    def getRangeString(self): return ",".join( "%d-%d"%(a,b) if a != b else "%d"%a for (a,b) in self._ltiRange )
    
    def iterPageNumber(self):
        """
        Iterator returning each page number in turn
        """    
        for a,b in self._ltiRange:
            for n in range(a,b+1):
                yield n
        raise StopIteration
    
    # -----    
    def __str__(self):
        return "%s=%s"%(self.sDocID, self.getRangeString())
        
def testDocPageSet():
    import pytest
    
    for s in ["111=1", "222=1-10", "333=1,10-20,23,40-50"]:
        assert str(DocPageSet(s)) == s, s
        
    o = DocPageSet("111=1")
    assert o.getDocID() == "111"
    assert [i for i in o.iterPageNumber()] == [1]

    o = DocPageSet("a/b/c/111=1")
    assert o.getDocID() == "a/b/c/111"
    assert o.getDocID(True) == "111"
    assert [i for i in o.iterPageNumber()] == [1]


    o = DocPageSet("333=1,10-20,23,40-50")
    assert o.getDocID() == "333"
    assert [i for i in o.iterPageNumber()] == [1]+range(10,21)+[23]+range(40,51)
    
    with pytest.raises(ValueError): DocPageSet("aaa")
    with pytest.raises(ValueError): DocPageSet("aaa=")
    with pytest.raises(ValueError): DocPageSet("=1")
    with pytest.raises(ValueError): DocPageSet("=1-2")
    with pytest.raises(ValueError): DocPageSet("aaa=12=12")
    with pytest.raises(ValueError): DocPageSet("aaa=22-11")
    with pytest.raises(ValueError): DocPageSet("aaa=-11")
    with pytest.raises(ValueError): DocPageSet("aaa=-11-")
    with pytest.raises(ValueError): DocPageSet("aaa=-11-12")
    with pytest.raises(ValueError): DocPageSet("aaa=333=1,10-20,3,40-50")

class PageXmlExtractor:
    '''
    Utility to extract several pages from several document to a folder
    '''
    sColDir = 'col'
    
    @classmethod
    def getFilename(self, sDocID, name):
        return os.path.join(sDocID, name)
        
    @classmethod
    def extractPagesToDir(cls, lDocPageSet, sToDir):
        """
        extract the pages from the given list of PageSet and store them in the given folder.
        (typically to be packaged as a MultiPageXml using PageXml.py)
        return the number of copied files, and list of tuple (pnum, orig-docID, orig-pnum, orig-filename)
        """
        if not os.path.isdir(sToDir):
            print(" - creating directory ", sToDir) 
            os.mkdir(sToDir) 
        else:
            if len(os.listdir(sToDir)) > 0: raise ValueError("Target folder (%s) must be empty."%sToDir)
        if not os.path.isdir(sToDir): raise ValueError("%s is not a directory"%sToDir) 

        jsonOriginFilename = os.path.join(sToDir, "origin.json")
        cnt, ltOrigin = cls.getOriginTuple(lDocPageSet, jsonOriginFilename)
               
        print( " - total number of pages = %d"%cnt)
        
        nbDigit = math.log10(cnt)+1
        sFmt = "%%0%dd.pxml" % nbDigit    #e.g. %03d.pxml
        
        for (cnt, docID, n, sFilename) in ltOrigin:
            sToFilename = os.path.join(sToDir, sFmt%cnt)
            print("   copying %s --> %s"%(sFilename, sToFilename))
            shutil.copy(sFilename, sToFilename)
        
        return cnt, ltOrigin
                    
    @classmethod
    def extractPagesToFile(cls, lDocPageSet, sToFile, bIndent=True):
        """
        extract the pages from the given list of PageSet and store them in a MultiPageXml file
        (typically to be packaged as a MultiPageXml using PageXml.py)
        return the number of copied files, and list of tuple (pnum, orig-docID, orig-pnum, orig-filename)
        """
        
        sBaseName, _ = os.path.splitext(sToFile)
        jsonOriginFilename = sBaseName + "_origin.json"
        cnt, ltOrigin = cls.getOriginTuple(lDocPageSet, jsonOriginFilename)
               
        print( " - total number of pages = %d"%cnt)
        
        print( "   Generating %s"%(sToFile))
        doc = PageXml.MultiPageXml.makeMultiPageXml([sFilename for (cnt, docID, n, sFilename) in ltOrigin] )
        doc.write(sToFile, xml_declaration='UTF-8',encoding="utf-8", pretty_print=bIndent)
        
        return cnt, ltOrigin
        
    @classmethod
    def getOriginTuple(cls, lDocPageSet, jsonOriginFilename=None):
        """
        prepare for extracting the pages from the given list of PageSet 
        return the number of files, and list of tuple (pnum, orig-docID, orig-pnum, orig-filename)
        """
        
        ltOrigin = list() 
        cnt = 0
        for o in lDocPageSet:
            print( " - Processing doc %s, pages %s"%(o.getDocID(), o.getRangeString()))
            lsFilename = cls.getPageFilenameList(o.getDocID(), ".pxml")
            for n in o.iterPageNumber():
                cnt += 1
                sFilename = lsFilename[n-1]
                ltOrigin.append( (cnt, o.getDocID(True), n, sFilename) ) # new-PNum, docID, orig-PNum, orig-filename

        if jsonOriginFilename:
            if sys.version_info > (3,0):
                with open(jsonOriginFilename, "wb",encoding='utf-8') as fd: json.dump(ltOrigin, fd, indent=True)
            else:
                with open(jsonOriginFilename, "wb") as fd: json.dump(ltOrigin, fd, indent=True)
                        
            print( "   (see %s)"%(jsonOriginFilename))
        
        return cnt, ltOrigin
        

    @classmethod
    def getPageFilenameList(cls, sDocID, sExt):
        assert sExt.startswith('.')
        
        #Look in trp.json file
        lsFilename = [] 

        trpFile = os.path.join(sDocID, 'trp.json')
        if not( os.path.exists(trpFile)): raise ValueError("Non-existing trp.json file %s" % trpFile)
        with open(trpFile, "rb",'utf-8') as fd: 
            jTrp = json.load(fd)
        
            for i, page in enumerate(jTrp['pageList']['pages']):
                sImgFileName = page['imgFileName']
                sBaseName, _ = os.path.splitext(sImgFileName)
                sXmlFilename = cls.getFilename(sDocID,  sBaseName + sExt)
                lsFilename .append( sXmlFilename )
                if page['pageNr'] != i+1: print( "\tWarning: expected page number %d , got %s"%(i+1, page['pageNr']))
            
        return lsFilename
    
if __name__ == "__main__":
    
    import sys, optparse
    usage = """
%s [--mpxml filename] [--dir dirname] [docID=<page-range-set>]+

Utility to extract a set of PageXml files from a set of documents and either:
- store them into a target folder with simple numbering, with unambiguous order.
- generate a MultiPageXMl document. In case of empty filename or "-", the filename is automatically composed from the arguments.  

a page-range-set takes the form: <pageRange>[,<pageRange>]+
 with pageRange taking the form: N|N-N
 Page ranges must be ordered, per document.
For instance: 111=1 222=1-10 333=1,10-20,23,40-50

JL Meunier - Aug. 2017
""" % sys.argv[0]

    parser = optparse.OptionParser(usage=usage)
    parser.add_option("--dir" ,  dest='dir' , action="store", type="string", help="Store the extracted PageXml pages into the specified directory.")    
    parser.add_option("--file",  dest='file', action="store", type="string", help="Store the extracted PageXml pages into the specified MultiPageXml document.")    
    
    (options, args) = parser.parse_args()

    if args:
        lsDocPageSet = args
    else:
        parser.print_help()
        parser.exit(1, "")
    
    lDocPageSet = []
    print("Parsing range(s)")
    for s in lsDocPageSet:
        o = DocPageSet(s)
        lDocPageSet.append(o)
    
    if options.dir:
        print( "Extracting into folder: ", options.dir)
        n = PageXmlExtractor.extractPagesToDir(lDocPageSet, options.dir)    
    
    if options.file != None:
        if options.file in["", "-"]: options.file = "extraction_" + "_".join(map(str, lDocPageSet))     #automatic filename
        sToFile = options.file if options.file.lower().endswith(".mpxml") else options.file+".mpxml"   #automatic .mpxml extension
        print( "Extracting into file: ", sToFile)
        n = PageXmlExtractor.extractPagesToFile(lDocPageSet, sToFile)    

    print( "DONE")
        