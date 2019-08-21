# -*- coding: utf-8 -*-
"""
    test DS2PageXml convertor
    @author:déjean
"""
import os.path
from xml_formats.DS2PageXml import DS2PageXMLConvertor
from xml_formats.PageXml import MultiPageXml

sTESTS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_DS2PageXmlConversion():
    filename = os.path.join(sTESTS_DIR,
                            'testDS2PageXml/RRB_MM_01_033_Jahr_1810.ds.xml')
    conv= DS2PageXMLConvertor()
    conv.inputFileName = filename
    doc = conv.loadDom(filename)
    lPageXmlDocs = conv.run(doc)
    mp = MultiPageXml()
    # newDoc = mp.makeMultiPageXmlMemory(map(lambda (x,y):x,lPageXmlDocs))
    newDoc = mp.makeMultiPageXmlMemory([x for x,_y in lPageXmlDocs])
    newDoc.write(os.path.join(sTESTS_DIR,
                              "testDS2PageXml/RRB_MM_01_033_Jahr_1810.mpxml"),
                 xml_declaration=True,
                 encoding="UTF-8",
                 pretty_print=True)


#     res= conv.storePageXmlSetofFiles(lPageXmlDocs)
#     print 'test:', True if res == 0  else False
    
if __name__ == "__main__":
#     test_setMetadata()
    test_DS2PageXmlConversion()