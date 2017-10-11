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
import copy

from common.DateTimeRange import DateTimeRange as DateTimeRangeSpec
from common.IntegerRange import IntegerRange

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
    
    def getTRP(self):
        return self.dic
    
    def getCollectionId(self):
        return self.dic["collection"]["colId"]
    
    def getNumberOfPages(self):
        return self.dic["md"]["nrOfPages"]
    
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
    
    def getTranscriptList(self):
        """
        return the concatenated list of transcripts per page of the document
        """
        return [ dTr for dPage in self.getPageList() for dTr in dPage["tsList"]["transcripts"] ]

    @classmethod
    def deepcopy(self):
        """
        deep copy of this object
        """
        return self.__class__( copy.deepcopy(self.dic) )

    def filterPageList(self, lPageNumberToKeep, bInPlace=True):
        """
        filter the list of pages to retain only those listed in the given list 
        
        lPageNumberToKeep must be a container of integers, and must support the __contains__ container method. (A PageRangeSpec object is fine, for instance ;-) )
        Note: this code is not optimal, but there is probably no performance gain to obtain here, and at least it is very legible.
        """
        o = self if bInPlace else self.deepcopy()

        ldPages = o.getPageList()
        ldPagesInRange = [ dPage for dPage in ldPages if dPage["pageNr"] in lPageNumberToKeep]
        
        o.setPageList(ldPagesInRange)
        return o

    def filterTranscriptsBySlot(self, oTimeSpec, slotname, bInPlace=True):
        """
        filter the list of pages to retain only those listed in the given list 
        
        Note: this code is not optimal, but there is probably no performance gain to obtain here, and at least it is very legible.
        """
        o = self if bInPlace else self.deepcopy()
        
        ldPages = o.getPageList()
        new_ldPages = list()    #we may have to discard pages without any transcript after filtering
        for dPage in ldPages:
            ldTr = dPage["tsList"]["transcripts"]
            new_ldTr = [dTr for dTr in ldTr if dTr[slotname] in oTimeSpec]
            if len(ldTr) != len(new_ldTr):
                dPage["tsList"]["transcripts"] = new_ldTr
            if new_ldTr:
                new_ldPages.append(dPage)
        o.setPageList(new_ldPages)
        return o
    
    def filterLastTranscript(self, bInPlace=True):
        """
        keep only the last transcipt of each page of the TRP
        """
        o = self if bInPlace else self.deepcopy()
        
        ldPages = o.getPageList()
        for dPage in ldPages:
            ldTr = dPage["tsList"]["transcripts"]
            if ldTr:
                #should always be the case
                new_ldTr = ldTr[0:1]    #keep the first
                if len(ldTr) != len(new_ldTr):
                    dPage["tsList"]["transcripts"] = new_ldTr
        return o
        
    def _getTranscriptSlotList(self, slot):
        """
        return the given slot value for each page, as a list of values
        """
        return [ tr[slot] for tr in self.getTranscriptList() ]
        
        
    def getTranscriptUsernameList(self):
        """
        Return the list of username (of last transcript of each page)
        """
        return self._getTranscriptSlotList("userName")

    def getTranscriptStatusList(self):
        """
        Return the list of status (of last transcript of each page)
        """
        return self._getTranscriptSlotList("status")

    def getTranscriptTimestampList(self):
        """
        Return the list of timestamp (of last transcript of each page)
        """
        return self._getTranscriptSlotList("timestamp")


    def report_short(self, warn=" ", bTSId=False):
        """
        return a string report
        """
        lt5 = [ (tr["pageNr"], tr['tsId'], tr["timestamp"], tr["status"], tr["userName"]) for tr in self.getTranscriptList() ]
        ls = list()
        prev_pnum = None
        for pnum, tsId, ts, st, u in lt5:
            if pnum == prev_pnum:
                spnum = "-     "
            else:
                spnum="p%5s"%pnum
            prev_pnum = pnum
            
            if bTSId:
                ls.append("%s %s %s %s %s  %s  %s"%(warn, spnum, tsId, ts, DateTimeRangeSpec.isoformat(ts), st, u))  #CSV-compliant syntax!! ;-)
            else:
                ls.append("%s %s %s %s  %s  %s"   %(warn, spnum      , ts, DateTimeRangeSpec.isoformat(ts), st, u))  #CSV-compliant syntax!! ;-)
        return "\n".join(ls)
    
    def report_stat(self):
        ls = []
        nbPage = self.getNumberOfPages()
        ls.append("stat: number of pages in document: %d"%nbPage)
        lTr = self.getTranscriptList()
        ls.append("stat: number of selected transcripts: %d"%len(lTr))

        #Pages
        name, slotName = ('number of     covered pages', 'pageNr')
        lValue = [tr[slotName] for tr in lTr]
        lUniqueValue = list(set(lValue))
        ls.append("stat: %s : %d : %s"%(name, len(lUniqueValue), IntegerRange().initFromEnumeration(lUniqueValue)))
        #indicate which pages were not considered at all
        lMissingPageNr = list(set(range(1, 1+nbPage)).difference(set(lUniqueValue)))
        ls.append("stat: %s : %d : %s"%("number of not covered pages", len(lMissingPageNr), IntegerRange().initFromEnumeration(lMissingPageNr)))
        
        lts = [tr["timestamp"] for tr in lTr]
        for opname, op in [("min", min), ("max", max)]:
            if lts:  #otherwise min and max have no meaning
                ts = op(lts)
                ls.append("stat: timestamp : %s=%s %s"%(opname, ts, DateTimeRangeSpec.isoformat(ts)))
                
        #for name, slotName  in [("user", "userName"), ("status", "status"), ('pages', 'pageNr')]:
        for name, slotName  in [("Listed user(s)", "userName"), ("listed status(es)", "status")]:
            lValue = [tr[slotName] for tr in lTr]
            lUniqueValue = list(set(lValue))
            lUniqueValue.sort()
            ls.append("stat: %s : %d : %s"%(name, len(lUniqueValue), " ".join([str(s).encode("utf-8") for s in lUniqueValue])))
    
        return "\n".join(ls)
    
