# -*- coding: utf-8 -*-

'''
Created on 23 Nov 2016

@author: meunier
'''
import pytest
from lxml import etree
from io import BytesIO

from xml_formats.PageXml import PageXml, PageXmlException


def test_custom():
    assert PageXml.parseCustomAttr("")    == {}
    assert PageXml.parseCustomAttr(" ")   == {}
    assert PageXml.parseCustomAttr("   ") == {}

    assert PageXml.parseCustomAttr("a {x:1;}")    == { 'a': { 'x':'1' } }
    assert PageXml.parseCustomAttr(" a {x:1;}")   == { 'a': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a {x:1;} ")   == { 'a': { 'x':'1' } }
    assert PageXml.parseCustomAttr(" a {x:1;} ")  == { 'a': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a {x:1 ;}")   == { 'a': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a {x:1 ; }")  == { 'a': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a { x:1 ; }") == { 'a': { 'x':'1' } }
    
    assert PageXml.parseCustomAttr("a{x:1;}")     == { 'a': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a{x:1 ;}")    == { 'a': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a{x:1 ; }")   == { 'a': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a{ x:1 ; }")  == { 'a': { 'x':'1' } }
    
    assert PageXml.parseCustomAttr("a,b{x:1;}")       == { 'a': { 'x':'1' }, 'b': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a, b{x:1 ;}")     == { 'a': { 'x':'1' }, 'b': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a , b{x:1 ; }")   == { 'a': { 'x':'1' }, 'b': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a ,b{ x:1 ; }")   == { 'a': { 'x':'1' }, 'b': { 'x':'1' } }
    assert PageXml.parseCustomAttr("a ,b { x:1 ; }")   == { 'a': { 'x':'1' }, 'b': { 'x':'1' } }
    
    assert PageXml.parseCustomAttr("a { x:1 ; y:2 }")   == { 'a': { 'x':'1', 'y':'2'} }
    assert PageXml.parseCustomAttr("a,b { x:1 ; y:2 }")   == { 'a': { 'x':'1', 'y':'2'}, 'b': { 'x':'1', 'y':'2'} }

    assert PageXml.parseCustomAttr("a {}")    == { 'a': { } }

    assert PageXml.parseCustomAttr("readingOrder {index:4;} structure {type:catch-word;}") == { 'readingOrder': { 'index':'4' }, 'structure':{'type':'catch-word'} }

def test_malformed_custom():
    with pytest.raises(ValueError): PageXml.parseCustomAttr("a {x1;}")
    with pytest.raises(ValueError): PageXml.parseCustomAttr("a x1;}")
    with pytest.raises(ValueError): PageXml.parseCustomAttr("a { x1;")
    with pytest.raises(ValueError): PageXml.parseCustomAttr("a { x1 }")
    
    #with pytest.raises(ValueError): PageXml.parseCustomAttr("a { x:1 }")  #should it fail?
    assert PageXml.parseCustomAttr("a { x:1  2}") == {'a': {'x': '1  2'}}

    #with pytest.raises(ValueError): PageXml.parseCustomAttr("a { x:1  2}")#should it fail? (or do we allow spaces in names or values?)
    assert PageXml.parseCustomAttr("  a b   {   x y : 1  2  }") == {'a b': {'x y': '1  2'}}
    
def test_getsetCustomAttr():
    sXml = b"""
            <TextRegion type="page-number" id="p1_region_1471502505726_2" custom="readingOrder {index:9;} structure {type:page-number;}">
                <Coords points="972,43 1039,43 1039,104 972,104"/>
            </TextRegion>
            """
    doc = etree.parse(BytesIO(sXml))
    nd = doc.getroot()
    assert PageXml.getCustomAttr(nd, "readingOrder", "index") == '9'
    assert PageXml.setCustomAttr(nd, "readingOrder", "index", 99) == 99
    assert PageXml.getCustomAttr(nd, "readingOrder", "index") == '99'

    assert PageXml.getCustomAttr(nd, "readingOrder") == {'index':'99'}
    
    assert PageXml.setCustomAttr(nd, "readingOrder", "toto", "zou") == "zou"
    assert PageXml.getCustomAttr(nd, "readingOrder", "toto") == 'zou'

    with pytest.raises(PageXmlException): PageXml.getCustomAttr(nd, "readingOrder", "axiste_pas")
    with pytest.raises(PageXmlException): PageXml.getCustomAttr(nd, "axiste_pas_non_plus", "axiste_pas")
    
def getMetadataTestDOM():
    sXml = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15/pagecontent.xsd">
            <Metadata>
                <Creator>Tilla</Creator>
                <Created>2016-08-18T13:35:08.252+07:00</Created>
                <LastChange>2016-12-01T09:53:39.610+01:00</LastChange>
            </Metadata>
            <Page imageFilename="MM_1_001_001.jpg" imageWidth="1277" imageHeight="3518" type="other">
                <ReadingOrder>
                    <OrderedGroup id="p1_ro_1480582418139" caption="Regions reading order">
                        <RegionRefIndexed index="0" regionRef="region_1471502505726_2"/>
                        <RegionRefIndexed index="1" regionRef="region_1471502509664_3"/>
                        <RegionRefIndexed index="2" regionRef="region_1471502512664_4"/>
                        <RegionRefIndexed index="3" regionRef="region_1471502516586_5"/>
                        <RegionRefIndexed index="4" regionRef="region_1471502522320_6"/>
                        <RegionRefIndexed index="5" regionRef="region_1471502528414_7"/>
                        <RegionRefIndexed index="6" regionRef="region_1471502534742_8"/>
                        <RegionRefIndexed index="7" regionRef="region_1471502539352_9"/>
                        <RegionRefIndexed index="8" regionRef="region_1471502542539_10"/>
                        <RegionRefIndexed index="9" regionRef="region_1471502547211_11"/>
                        <RegionRefIndexed index="10" regionRef="region_1471502550274_12"/>
                        <RegionRefIndexed index="11" regionRef="region_1480582401040_1"/>
                    </OrderedGroup>
                </ReadingOrder>
            </Page>
        </PcGts>"""
    doc = etree.parse(BytesIO(sXml))
    return doc

def test_getMetadata():
    doc = getMetadataTestDOM()
    nd = doc.getroot()
    
    md = PageXml.getMetadata(doc)
    assert md.Creator == "Tilla"
    assert md.Created == "2016-08-18T13:35:08.252+07:00"
    assert md.LastChange == "2016-12-01T09:53:39.610+01:00"
    assert md.Comments == None
   
    md = PageXml.getMetadata(None, nd[0])
    assert md.Creator == "Tilla"
    assert md.Created == "2016-08-18T13:35:08.252+07:00"
    assert md.LastChange == "2016-12-01T09:53:39.610+01:00"
    
def test_setMetadata():
    import datetime
    doc = getMetadataTestDOM()

    nd = doc.getroot()
    _sutc = datetime.datetime.utcnow().isoformat()
    PageXml.setMetadata(doc, None, "Tigrette")
    
    sutc = datetime.datetime.utcnow().isoformat()
    md = PageXml.getMetadata(doc)
    assert md.Creator == "Tigrette"
    assert md.Created == "2016-08-18T13:35:08.252+07:00"
    assert md.LastChange.startswith(sutc[:15])
    assert md.Comments == None
    print(doc)
   
    sutc = datetime.datetime.utcnow().isoformat()
    PageXml.setMetadata(doc, None, "Bijoux", "Le chat de Martine")
    md = PageXml.getMetadata(None, nd[0])
    assert md.Creator == "Bijoux"
    assert md.Created == "2016-08-18T13:35:08.252+07:00"
    assert md.LastChange.startswith(sutc[:15])
    assert md.Comments == "Le chat de Martine"
    print(doc)
    
def test_CreationPageXmlDocument():
    doc= PageXml.createPageXmlDocument(creatorName='HerveforTest', filename='hervefortest.jpg', imgW=100, imgH=100)
    print(doc)
    
if __name__ == "__main__":
    test_setMetadata()
    test_CreationPageXmlDocument()