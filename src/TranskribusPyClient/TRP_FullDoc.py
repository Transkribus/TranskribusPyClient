# -*- coding: utf-8 -*-

"""
    Utility class to parse and operate on JSON data sent by getDocById() === GET/collections/{collId}/{id}/fulldoc
    
    Copyright Naver(C) 2017, JL. Meunier, August 2017

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
import types

class TRP_FullDoc:
    """
    A JSON data structure describing a full document
    
    Something like:

{
    "collection": {
        "colId": 7018,
        "colName": "BAR_DU-testcollection",
        "crowdsourcing": false,
        "description": "created by tobias.hodel@uzh.ch",
        "elearning": false,
        "nrOfDocuments": 0
    },
    "edDeclList": [],
    "md": {
        "collectionList": {
            "colList": [
                {
                    "colId": 7018,
                    "colName": "BAR_DU-testcollection",
                    "crowdsourcing": false,
                    "description": "created by tobias.hodel@uzh.ch",
                    "elearning": false,
                    "nrOfDocuments": 0
                }
            ]
        },
        "createdFromTimestamp": 0,
        "createdToTimestamp": 0,
        "docId": 23691,
        "fimgStoreColl": "TrpDoc_DEA_23691",
        "nrOfPages": 1875,
        "scriptType": "GOTHIC",
        "status": 0,
        "title": "BAR_1867",
        "uploadTimestamp": 1500437704364,
        "uploader": "tobias.hodel@uzh.ch",
        "uploaderId": 537
    },
    "pageList": {
        "pages": [
            {
                "created": "2017-07-19T06:15:04.556+02:00",
                "docId": 23691,
                "height": 4963,
                "imageId": 517694,
                "imageVersions": {
                    "imageVersions": []
                },
                "imgFileName": "70004181_70004181-0.jpg",
                "indexed": true,
                "key": "LRWPUTWIEYSEPAPUBEDVMLJI",
                "pageId": 637242,
                "pageNr": 1,
                "tagsStored": "2017-08-22T10:44:23.106+02:00",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=LRWPUTWIEYSEPAPUBEDVMLJI&fileType=thumb",
                "tsList": {
                    "transcripts": [
                        {
                            "docId": 23691,
                            "key": "RFPAPVAPPMPDCGPAYFIHEBJF",
                            "md5Sum": "",
                            "nrOfLines": 54,
                            "nrOfRegions": 23,
                            "nrOfTranscribedLines": 0,
                            "nrOfTranscribedRegions": 0,
                            "nrOfTranscribedWords": 0,
                            "nrOfWords": 0,
                            "nrOfWordsInLines": 0,
                            "nrOfWordsInRegions": 0,
                            "pageId": 637242,
                            "pageNr": 1,
                            "parentTsId": -1,
                            "status": "IN_PROGRESS",
                            "timestamp": 1503314055520,
                            "toolName": "NCSR_tS_LA 1.1",
                            "tsId": 1085663,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=RFPAPVAPPMPDCGPAYFIHEBJF",
                            "userId": 3556,
                            "userName": "jean-luc.meunier@naverlabs.com"
                        },
                        {
                            "docId": 23691,
                            "key": "LDNETZPWFAJXNIZNNWCLEBZN",
                            "md5Sum": "",
                            "nrOfLines": 0,
                            "nrOfRegions": 23,
                            "nrOfTranscribedLines": 0,
                            "nrOfTranscribedRegions": 0,
                            "nrOfTranscribedWords": 0,
                            "nrOfWords": 0,
                            "nrOfWordsInLines": 0,
                            "nrOfWordsInRegions": 0,
                            "pageId": 637242,
                            "pageNr": 1,
                            "parentTsId": 1005505,
                            "status": "NEW",
                            "timestamp": 1501070277819,
                            "tsId": 1028862,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=LDNETZPWFAJXNIZNNWCLEBZN",
                            "userId": 6625,
                            "userName": "martastrasse@vtxmail.ch"
                        }
                    ]
                },
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=LRWPUTWIEYSEPAPUBEDVMLJI&fileType=view",
                "width": 3508
            }
            
        ... next pages here ...
        ]
    }
}
"""
    
    def __init__(self, jsonTRP):
        """
        pass the JSON data
        """
        self.dic = jsonTRP
        
    def getPageList(self):
        """
        return the (mutable) list of page dictionaries
        """
        return self.dic["pageList"]["pages"]
    
    def setPageList(self, lPageDic):
        """
        set the list of page dictionaries
        return it
        """
        self.dic["pageList"]["pages"] = lPageDic
        return lPageDic
    
    def filterPageList(self, lPageNumberToKeep):
        """
        filter the list of pages to retain only those listed in the given list 
        
        lPageNumberToKeep must be a container of integers, and must support the __contains__ container method. (A PageRangeSpec object is fine, for instance ;-) )
        Note: this code is not optimal, but there is probably no performance gain to obtain here, and at least it is very legible.
        """
        ldPages = self.getPageList()
        ldPagesInRange = [ dPage for dPage in ldPages if dPage["pageNr"] in lPageNumberToKeep]
        return self.setPageList(ldPagesInRange)

#     def __str__(self): return ",".join( "%d-%d"%(a,b) if a != b else "%d"%a for (a,b) in self._ltAB )
#     
#     #Emulating Container type...
#     def __iter__(self):
#         """
#         Iterator returning each page number in turn
#         """    
#         for a,b in self._ltAB:
#             for n in range(a,b+1): yield n
#         raise StopIteration
#     
#     def __reversed__(self):
#         """
#         Reversed iterator
#         If we do not provide it, we must provide a __getitem__ (boring to code and how useful??)
#         """
#         for a,b in reversed(self._ltAB):
#             for n in range(b,a-1,-1): yield n
#         raise StopIteration        
#         
#     def __len__(self):
#         return sum(b-a+1 for a,b in self._ltAB)
# 
#     def __contains__(self, item):
#         if type(item) != types.IntType: raise ValueError("A page range contains integer values not %s"%type(item))
#         a, b = None, None
#         for a,b in self._ltAB:
#             if b >= item: break
#         return a<= item and item <= b
# 
# def test_good_spec(capsys):
#     def container_test(o, lref):
#         assert list(o) == lref
#         assert list(reversed(o)) == list(reversed(lref))
#         for item in lref: assert item in o
#         assert -99 not in o
#         
#     o = PageRangeSpec("1")
# #     with capsys.disabled():
# #         print "YOOOOOOOOOOOOOOOOOOOOOOOOOOO ", list(reversed(o))    
#     container_test(o, [1])
#     
#     o = PageRangeSpec("99")
#     container_test(o, [99])    
#     
#     o = PageRangeSpec("1,99")
#     container_test(o, [1, 99])      
#     
#     o = PageRangeSpec("1-5")
#     container_test(o, range(1, 6))
# 
#     o = PageRangeSpec("1-5,6-88")
#     container_test(o, range(1, 6)+range(6, 89))          
#     
#     o = PageRangeSpec("1-3,4-8")
#     container_test(o, range(1, 9))   
#     assert len(o) == len(range(1, 9)) 
# 
# def test_spaced_good_spec():
#     def container_test(o, lref):
#         assert list(o) == lref
#         assert list(reversed(o))== list(reversed(lref))
#         for item in lref: assert item in o
#         assert -99 not in o
#         
#     o = PageRangeSpec(" 1\t\t")
#     container_test(o, [1])
#     
#     o = PageRangeSpec("99  ")
#     container_test(o, [99])    
#     
#     o = PageRangeSpec("1  , 99")
#     container_test(o, [1, 99])      
#     
#     o = PageRangeSpec(" 1\t- 5\t")
#     container_test(o, range(1, 6))
# 
#     o = PageRangeSpec("1-5, 6-88")
#     container_test(o, range(1, 6)+range(6, 89))          
#     
#     o = PageRangeSpec("1 -3\t,4- 8")
#     container_test(o, range(1, 9))
#     assert len(o) == len(range(1, 9)) 
# 
# def test_errors():
#     import pytest
#     with pytest.raises(ValueError): PageRangeSpec("1 3")
#     with pytest.raises(ValueError): PageRangeSpec("3-1")
#     with pytest.raises(ValueError): PageRangeSpec("3,1")
#     with pytest.raises(ValueError): PageRangeSpec("1-3,2")
#     with pytest.raises(ValueError): PageRangeSpec("3,1-2")
#     with pytest.raises(ValueError): PageRangeSpec("1-3,3-8")
#     with pytest.raises(ValueError): PageRangeSpec("1-3 3,3-8")
#     with pytest.raises(ValueError): PageRangeSpec("1-3,3-8 8")
#     
# 
# def test_limit():
#     o = PageRangeSpec("")
#     assert list(o) == []
#     assert len(o) == 0
#     o = PageRangeSpec("\t  \t ")
#     assert list(o) == []
#     assert len(o) == 0    
#     
