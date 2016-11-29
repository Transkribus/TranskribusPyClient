# -*- coding: utf-8 -*-

#optional: useful if you want to choose the logging level to something else than logging.WARN
import logging

from read.TranskribusPyClient.test import _colId_A, _docId_b
from read.TranskribusPyClient.client import TranskribusClient, getStoredCredentials

login, pwd = getStoredCredentials()

conn = TranskribusClient(proxies={'https':'http://cornillon:8000'}
                         , loggingLevel=logging.INFO)
print conn

#print conn.auth_logout()

sessionID = conn.auth_login(login, pwd)
print sessionID

#sessionID = conn.auth_login("jean-luc.meunier@xrce.xerox.com", "trnjluc", sHttpsProxyUrl='http://cornillon:8000')



# ret = conn.getDocumentFromServer(colid, docid)
#ret = conn.getDocumentFromServer("3571", "7750")
data = conn.collections_fulldoc(_colId_A, _docId_b)
print data


conn.setProxies({'https':'http://cornillon:8000'})

print conn.auth_logout()

"""
{
    "md": {
        "docId": 7750,
        "title": "MM_1_005",
        "uploadTimestamp": 1478161451242,
        "scriptType": "HANDWRITTEN",
        "uploader": "herve.dejean@xrce.xerox.com",
        "uploaderId": 275,
        "nrOfPages": 10,
        "status": 0,
        "fimgStoreColl": "TrpDoc_DEA_7750",
        "createdFromTimestamp": 0,
        "createdToTimestamp": 0,
        "collectionList": {
            "colList": [
                {
                    "colId": 3571,
                    "colName": "READDU",
                    "description": "created by herve.dejean@xrce.xerox.com"
                }
            ]
        }
    },
    "pageList": {
        "pages": [
            {
                "pageId": 241858,
                "docId": 7750,
                "pageNr": 1,
                "key": "DJVKXRYFHSVIDXQXIQIDYEII",
                "imageId": 227134,
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=DJVKXRYFHSVIDXQXIQIDYEII&fileType=view",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=DJVKXRYFHSVIDXQXIQIDYEII&fileType=thumb",
                "imgFileName": "MM_1_005_001.jpg",
                "tsList": {
                    "transcripts": [
                        {
                            "tsId": 381516,
                            "parentTsId": 381511,
                            "key": "FDQJTHVXETZGWOTJERYTXTQF",
                            "pageId": 241858,
                            "docId": 7750,
                            "pageNr": 1,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=FDQJTHVXETZGWOTJERYTXTQF",
                            "status": "GT",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478165176495,
                            "md5Sum": "",
                            "nrOfRegions": 5,
                            "nrOfTranscribedRegions": 5,
                            "nrOfWordsInRegions": 163,
                            "nrOfLines": 59,
                            "nrOfTranscribedLines": 59,
                            "nrOfWordsInLines": 217,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381511,
                            "parentTsId": 381509,
                            "key": "IEDZSBGJXDDXTNJUUQBYTAOE",
                            "pageId": 241858,
                            "docId": 7750,
                            "pageNr": 1,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=IEDZSBGJXDDXTNJUUQBYTAOE",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478165121979,
                            "md5Sum": "",
                            "nrOfRegions": 5,
                            "nrOfTranscribedRegions": 5,
                            "nrOfWordsInRegions": 163,
                            "nrOfLines": 59,
                            "nrOfTranscribedLines": 59,
                            "nrOfWordsInLines": 217,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381509,
                            "parentTsId": 381506,
                            "key": "NOHPHKSASMUXUUZADVNFTJWY",
                            "pageId": 241858,
                            "docId": 7750,
                            "pageNr": 1,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=NOHPHKSASMUXUUZADVNFTJWY",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478165078290,
                            "md5Sum": "",
                            "nrOfRegions": 5,
                            "nrOfTranscribedRegions": 5,
                            "nrOfWordsInRegions": 163,
                            "nrOfLines": 59,
                            "nrOfTranscribedLines": 59,
                            "nrOfWordsInLines": 217,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381506,
                            "parentTsId": 381363,
                            "key": "XCJJGBTIWVNHBEAJCSNURLVQ",
                            "pageId": 241858,
                            "docId": 7750,
                            "pageNr": 1,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=XCJJGBTIWVNHBEAJCSNURLVQ",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478164989861,
                            "md5Sum": "",
                            "nrOfRegions": 5,
                            "nrOfTranscribedRegions": 5,
                            "nrOfWordsInRegions": 163,
                            "nrOfLines": 59,
                            "nrOfTranscribedLines": 59,
                            "nrOfWordsInLines": 217,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381363,
                            "parentTsId": -1,
                            "key": "FMKDLHJQTWVDQOAQBEYMBODW",
                            "pageId": 241858,
                            "docId": 7750,
                            "pageNr": 1,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=FMKDLHJQTWVDQOAQBEYMBODW",
                            "status": "NEW",
                            "userName": "herve.dejean@xrce.xerox.com",
                            "userId": 275,
                            "timestamp": 1478161451242,
                            "md5Sum": "",
                            "nrOfRegions": 5,
                            "nrOfTranscribedRegions": 5,
                            "nrOfWordsInRegions": 163,
                            "nrOfLines": 59,
                            "nrOfTranscribedLines": 59,
                            "nrOfWordsInLines": 217,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        }
                    ]
                },
                "width": 1079,
                "height": 3505,
                "created": "2016-11-03T09:24:11.649+01:00",
                "indexed": true
            },
            {
                "pageId": 241859,
                "docId": 7750,
                "pageNr": 2,
                "key": "DBFNKQONQBWKKUCODOFAXTXN",
                "imageId": 227135,
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=DBFNKQONQBWKKUCODOFAXTXN&fileType=view",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=DBFNKQONQBWKKUCODOFAXTXN&fileType=thumb",
                "imgFileName": "MM_1_005_002.jpg",
                "tsList": {
                    "transcripts": [
                        {
                            "tsId": 382132,
                            "parentTsId": 382121,
                            "key": "OODGHWRQMUWYYMNFCHJJBBDF",
                            "pageId": 241859,
                            "docId": 7750,
                            "pageNr": 2,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=OODGHWRQMUWYYMNFCHJJBBDF",
                            "status": "GT",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189886242,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 175,
                            "nrOfLines": 70,
                            "nrOfTranscribedLines": 70,
                            "nrOfWordsInLines": 238,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 382121,
                            "parentTsId": 382120,
                            "key": "PXZLJGZRNRXRNHHBIQBCTQWW",
                            "pageId": 241859,
                            "docId": 7750,
                            "pageNr": 2,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=PXZLJGZRNRXRNHHBIQBCTQWW",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189302829,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 175,
                            "nrOfLines": 70,
                            "nrOfTranscribedLines": 70,
                            "nrOfWordsInLines": 238,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 382120,
                            "parentTsId": 381513,
                            "key": "SJNLYFZWQDEIESMTDFDKWFEU",
                            "pageId": 241859,
                            "docId": 7750,
                            "pageNr": 2,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=SJNLYFZWQDEIESMTDFDKWFEU",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189247739,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 175,
                            "nrOfLines": 70,
                            "nrOfTranscribedLines": 70,
                            "nrOfWordsInLines": 238,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381513,
                            "parentTsId": 381364,
                            "key": "IWYPBOPZBTGPZUFHFHUYVIWL",
                            "pageId": 241859,
                            "docId": 7750,
                            "pageNr": 2,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=IWYPBOPZBTGPZUFHFHUYVIWL",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478165159816,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 175,
                            "nrOfLines": 70,
                            "nrOfTranscribedLines": 70,
                            "nrOfWordsInLines": 238,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381364,
                            "parentTsId": -1,
                            "key": "XXJNWCMCUINNSHDULAZBQRTS",
                            "pageId": 241859,
                            "docId": 7750,
                            "pageNr": 2,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=XXJNWCMCUINNSHDULAZBQRTS",
                            "status": "NEW",
                            "userName": "herve.dejean@xrce.xerox.com",
                            "userId": 275,
                            "timestamp": 1478161451242,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 175,
                            "nrOfLines": 70,
                            "nrOfTranscribedLines": 70,
                            "nrOfWordsInLines": 238,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        }
                    ]
                },
                "width": 1104,
                "height": 3513,
                "created": "2016-11-03T09:24:13.43+01:00",
                "indexed": true
            },
            {
                "pageId": 241860,
                "docId": 7750,
                "pageNr": 3,
                "key": "UDRRJBUZDRXDFIQRPZKJKSWH",
                "imageId": 227136,
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=UDRRJBUZDRXDFIQRPZKJKSWH&fileType=view",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=UDRRJBUZDRXDFIQRPZKJKSWH&fileType=thumb",
                "imgFileName": "MM_1_005_003.jpg",
                "tsList": {
                    "transcripts": [
                        {
                            "tsId": 382133,
                            "parentTsId": 382123,
                            "key": "LXDEPITAWFETAMURDTRIEAQL",
                            "pageId": 241860,
                            "docId": 7750,
                            "pageNr": 3,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=LXDEPITAWFETAMURDTRIEAQL",
                            "status": "GT",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189896358,
                            "md5Sum": "",
                            "nrOfRegions": 6,
                            "nrOfTranscribedRegions": 6,
                            "nrOfWordsInRegions": 167,
                            "nrOfLines": 60,
                            "nrOfTranscribedLines": 60,
                            "nrOfWordsInLines": 221,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 382123,
                            "parentTsId": 381365,
                            "key": "PPGLFICJMYPQCAZDPMKTDCJX",
                            "pageId": 241860,
                            "docId": 7750,
                            "pageNr": 3,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=PPGLFICJMYPQCAZDPMKTDCJX",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189576221,
                            "md5Sum": "",
                            "nrOfRegions": 6,
                            "nrOfTranscribedRegions": 6,
                            "nrOfWordsInRegions": 167,
                            "nrOfLines": 60,
                            "nrOfTranscribedLines": 60,
                            "nrOfWordsInLines": 221,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381365,
                            "parentTsId": -1,
                            "key": "SKBCTBWMQJJQBZKEQCXOEAXF",
                            "pageId": 241860,
                            "docId": 7750,
                            "pageNr": 3,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=SKBCTBWMQJJQBZKEQCXOEAXF",
                            "status": "NEW",
                            "userName": "herve.dejean@xrce.xerox.com",
                            "userId": 275,
                            "timestamp": 1478161451242,
                            "md5Sum": "",
                            "nrOfRegions": 6,
                            "nrOfTranscribedRegions": 6,
                            "nrOfWordsInRegions": 167,
                            "nrOfLines": 60,
                            "nrOfTranscribedLines": 60,
                            "nrOfWordsInLines": 221,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        }
                    ]
                },
                "width": 1126,
                "height": 3501,
                "created": "2016-11-03T09:24:15.377+01:00",
                "indexed": true
            },
            {
                "pageId": 241861,
                "docId": 7750,
                "pageNr": 4,
                "key": "YBLJLBUPWCSQVCNAWFYCCLRI",
                "imageId": 227137,
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=YBLJLBUPWCSQVCNAWFYCCLRI&fileType=view",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=YBLJLBUPWCSQVCNAWFYCCLRI&fileType=thumb",
                "imgFileName": "MM_1_005_004.jpg",
                "tsList": {
                    "transcripts": [
                        {
                            "tsId": 382134,
                            "parentTsId": 382124,
                            "key": "FFQJHLCOMGPWMEAGBVRQRQDY",
                            "pageId": 241861,
                            "docId": 7750,
                            "pageNr": 4,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=FFQJHLCOMGPWMEAGBVRQRQDY",
                            "status": "GT",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189902824,
                            "md5Sum": "",
                            "nrOfRegions": 5,
                            "nrOfTranscribedRegions": 5,
                            "nrOfWordsInRegions": 139,
                            "nrOfLines": 45,
                            "nrOfTranscribedLines": 45,
                            "nrOfWordsInLines": 179,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 382124,
                            "parentTsId": 381366,
                            "key": "EVAURZXRDFXCBOEVPEYHJMWQ",
                            "pageId": 241861,
                            "docId": 7750,
                            "pageNr": 4,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=EVAURZXRDFXCBOEVPEYHJMWQ",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189629364,
                            "md5Sum": "",
                            "nrOfRegions": 5,
                            "nrOfTranscribedRegions": 5,
                            "nrOfWordsInRegions": 139,
                            "nrOfLines": 45,
                            "nrOfTranscribedLines": 45,
                            "nrOfWordsInLines": 179,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381366,
                            "parentTsId": -1,
                            "key": "LWVMPOQDBYVZYTEJTYGGUSMJ",
                            "pageId": 241861,
                            "docId": 7750,
                            "pageNr": 4,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=LWVMPOQDBYVZYTEJTYGGUSMJ",
                            "status": "NEW",
                            "userName": "herve.dejean@xrce.xerox.com",
                            "userId": 275,
                            "timestamp": 1478161451242,
                            "md5Sum": "",
                            "nrOfRegions": 5,
                            "nrOfTranscribedRegions": 5,
                            "nrOfWordsInRegions": 139,
                            "nrOfLines": 45,
                            "nrOfTranscribedLines": 45,
                            "nrOfWordsInLines": 179,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        }
                    ]
                },
                "width": 1103,
                "height": 3518,
                "created": "2016-11-03T09:24:17.725+01:00",
                "indexed": true
            },
            {
                "pageId": 241862,
                "docId": 7750,
                "pageNr": 5,
                "key": "KBKXJPVJZPYRDEVOFEZYWLBV",
                "imageId": 227138,
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=KBKXJPVJZPYRDEVOFEZYWLBV&fileType=view",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=KBKXJPVJZPYRDEVOFEZYWLBV&fileType=thumb",
                "imgFileName": "MM_1_005_005.jpg",
                "tsList": {
                    "transcripts": [
                        {
                            "tsId": 382136,
                            "parentTsId": 382125,
                            "key": "RSVUGJANXAOJVCLKWNIHYOOF",
                            "pageId": 241862,
                            "docId": 7750,
                            "pageNr": 5,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=RSVUGJANXAOJVCLKWNIHYOOF",
                            "status": "GT",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478190125606,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 119,
                            "nrOfLines": 46,
                            "nrOfTranscribedLines": 46,
                            "nrOfWordsInLines": 158,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 382125,
                            "parentTsId": 381367,
                            "key": "GGUZKGAVPNRAPTLODBDJQREM",
                            "pageId": 241862,
                            "docId": 7750,
                            "pageNr": 5,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=GGUZKGAVPNRAPTLODBDJQREM",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189670357,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 119,
                            "nrOfLines": 46,
                            "nrOfTranscribedLines": 46,
                            "nrOfWordsInLines": 158,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381367,
                            "parentTsId": -1,
                            "key": "TKSXYLWVHFQXSSTFNUCHOJZZ",
                            "pageId": 241862,
                            "docId": 7750,
                            "pageNr": 5,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=TKSXYLWVHFQXSSTFNUCHOJZZ",
                            "status": "NEW",
                            "userName": "herve.dejean@xrce.xerox.com",
                            "userId": 275,
                            "timestamp": 1478161451242,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 119,
                            "nrOfLines": 46,
                            "nrOfTranscribedLines": 46,
                            "nrOfWordsInLines": 158,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        }
                    ]
                },
                "width": 1109,
                "height": 3495,
                "created": "2016-11-03T09:24:19.347+01:00",
                "indexed": true
            },
            {
                "pageId": 241863,
                "docId": 7750,
                "pageNr": 6,
                "key": "EXNNKQHSFSZFUSFWHJHSGLFL",
                "imageId": 227139,
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=EXNNKQHSFSZFUSFWHJHSGLFL&fileType=view",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=EXNNKQHSFSZFUSFWHJHSGLFL&fileType=thumb",
                "imgFileName": "MM_1_005_006.jpg",
                "tsList": {
                    "transcripts": [
                        {
                            "tsId": 382137,
                            "parentTsId": 382126,
                            "key": "CDIHCQRVKWJQIUFMVKZAZAKZ",
                            "pageId": 241863,
                            "docId": 7750,
                            "pageNr": 6,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=CDIHCQRVKWJQIUFMVKZAZAKZ",
                            "status": "GT",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478190132430,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 143,
                            "nrOfLines": 58,
                            "nrOfTranscribedLines": 58,
                            "nrOfWordsInLines": 194,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 382126,
                            "parentTsId": 381368,
                            "key": "WLOWSZLXIDSBGNWXNWXDVMDY",
                            "pageId": 241863,
                            "docId": 7750,
                            "pageNr": 6,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=WLOWSZLXIDSBGNWXNWXDVMDY",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189729174,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 143,
                            "nrOfLines": 58,
                            "nrOfTranscribedLines": 58,
                            "nrOfWordsInLines": 194,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381368,
                            "parentTsId": -1,
                            "key": "GIGTEQVBSZUXDVXLGKBMOUIZ",
                            "pageId": 241863,
                            "docId": 7750,
                            "pageNr": 6,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=GIGTEQVBSZUXDVXLGKBMOUIZ",
                            "status": "NEW",
                            "userName": "herve.dejean@xrce.xerox.com",
                            "userId": 275,
                            "timestamp": 1478161451242,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 143,
                            "nrOfLines": 58,
                            "nrOfTranscribedLines": 58,
                            "nrOfWordsInLines": 194,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        }
                    ]
                },
                "width": 1143,
                "height": 3513,
                "created": "2016-11-03T09:24:20.817+01:00",
                "indexed": true
            },
            {
                "pageId": 241864,
                "docId": 7750,
                "pageNr": 7,
                "key": "LPTQSNRVVPFERXFQUZVYJZJT",
                "imageId": 227140,
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=LPTQSNRVVPFERXFQUZVYJZJT&fileType=view",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=LPTQSNRVVPFERXFQUZVYJZJT&fileType=thumb",
                "imgFileName": "MM_1_005_007.jpg",
                "tsList": {
                    "transcripts": [
                        {
                            "tsId": 382138,
                            "parentTsId": 382127,
                            "key": "AJBVJHMJRZWTBTBTZASIEYON",
                            "pageId": 241864,
                            "docId": 7750,
                            "pageNr": 7,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=AJBVJHMJRZWTBTBTZASIEYON",
                            "status": "GT",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478190139565,
                            "md5Sum": "",
                            "nrOfRegions": 4,
                            "nrOfTranscribedRegions": 4,
                            "nrOfWordsInRegions": 130,
                            "nrOfLines": 44,
                            "nrOfTranscribedLines": 44,
                            "nrOfWordsInLines": 170,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 382127,
                            "parentTsId": 381369,
                            "key": "PIZEKVZKEQCBESCCICXYXWWC",
                            "pageId": 241864,
                            "docId": 7750,
                            "pageNr": 7,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=PIZEKVZKEQCBESCCICXYXWWC",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189755562,
                            "md5Sum": "",
                            "nrOfRegions": 4,
                            "nrOfTranscribedRegions": 4,
                            "nrOfWordsInRegions": 130,
                            "nrOfLines": 44,
                            "nrOfTranscribedLines": 44,
                            "nrOfWordsInLines": 170,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381369,
                            "parentTsId": -1,
                            "key": "UWMMSHFVNELGGQMFODYGZFIA",
                            "pageId": 241864,
                            "docId": 7750,
                            "pageNr": 7,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=UWMMSHFVNELGGQMFODYGZFIA",
                            "status": "NEW",
                            "userName": "herve.dejean@xrce.xerox.com",
                            "userId": 275,
                            "timestamp": 1478161451242,
                            "md5Sum": "",
                            "nrOfRegions": 4,
                            "nrOfTranscribedRegions": 4,
                            "nrOfWordsInRegions": 130,
                            "nrOfLines": 44,
                            "nrOfTranscribedLines": 44,
                            "nrOfWordsInLines": 170,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        }
                    ]
                },
                "width": 1121,
                "height": 3479,
                "created": "2016-11-03T09:24:22.372+01:00",
                "indexed": true
            },
            {
                "pageId": 241865,
                "docId": 7750,
                "pageNr": 8,
                "key": "VATMDYPWNWSZKBZYSWLWIXZZ",
                "imageId": 227141,
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=VATMDYPWNWSZKBZYSWLWIXZZ&fileType=view",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=VATMDYPWNWSZKBZYSWLWIXZZ&fileType=thumb",
                "imgFileName": "MM_1_005_008.jpg",
                "tsList": {
                    "transcripts": [
                        {
                            "tsId": 382139,
                            "parentTsId": 382128,
                            "key": "AIWLPBSWUHABYPSGEPIYBDXY",
                            "pageId": 241865,
                            "docId": 7750,
                            "pageNr": 8,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=AIWLPBSWUHABYPSGEPIYBDXY",
                            "status": "GT",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478190145477,
                            "md5Sum": "",
                            "nrOfRegions": 8,
                            "nrOfTranscribedRegions": 8,
                            "nrOfWordsInRegions": 146,
                            "nrOfLines": 60,
                            "nrOfTranscribedLines": 60,
                            "nrOfWordsInLines": 198,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 382128,
                            "parentTsId": 381370,
                            "key": "FPSNGGWEVYVHOZXTHEDCZRRS",
                            "pageId": 241865,
                            "docId": 7750,
                            "pageNr": 8,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=FPSNGGWEVYVHOZXTHEDCZRRS",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189777858,
                            "md5Sum": "",
                            "nrOfRegions": 8,
                            "nrOfTranscribedRegions": 8,
                            "nrOfWordsInRegions": 146,
                            "nrOfLines": 60,
                            "nrOfTranscribedLines": 60,
                            "nrOfWordsInLines": 198,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381370,
                            "parentTsId": -1,
                            "key": "COZMHQZMYPYNSQNXDNHONHEI",
                            "pageId": 241865,
                            "docId": 7750,
                            "pageNr": 8,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=COZMHQZMYPYNSQNXDNHONHEI",
                            "status": "NEW",
                            "userName": "herve.dejean@xrce.xerox.com",
                            "userId": 275,
                            "timestamp": 1478161451242,
                            "md5Sum": "",
                            "nrOfRegions": 8,
                            "nrOfTranscribedRegions": 8,
                            "nrOfWordsInRegions": 146,
                            "nrOfLines": 60,
                            "nrOfTranscribedLines": 60,
                            "nrOfWordsInLines": 198,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        }
                    ]
                },
                "width": 1125,
                "height": 3489,
                "created": "2016-11-03T09:24:24.404+01:00",
                "indexed": true
            },
            {
                "pageId": 241866,
                "docId": 7750,
                "pageNr": 9,
                "key": "CBNMUJLYGDPZFFVLHMWHXATI",
                "imageId": 227142,
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=CBNMUJLYGDPZFFVLHMWHXATI&fileType=view",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=CBNMUJLYGDPZFFVLHMWHXATI&fileType=thumb",
                "imgFileName": "MM_1_005_009.jpg",
                "tsList": {
                    "transcripts": [
                        {
                            "tsId": 382140,
                            "parentTsId": 382129,
                            "key": "WFCLYZBVQOLRYFDHMUHSAXIB",
                            "pageId": 241866,
                            "docId": 7750,
                            "pageNr": 9,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=WFCLYZBVQOLRYFDHMUHSAXIB",
                            "status": "GT",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478190151621,
                            "md5Sum": "",
                            "nrOfRegions": 6,
                            "nrOfTranscribedRegions": 6,
                            "nrOfWordsInRegions": 136,
                            "nrOfLines": 45,
                            "nrOfTranscribedLines": 45,
                            "nrOfWordsInLines": 175,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 382129,
                            "parentTsId": 381371,
                            "key": "PSKXONHHRETXTHOZRRYKTUUK",
                            "pageId": 241866,
                            "docId": 7750,
                            "pageNr": 9,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=PSKXONHHRETXTHOZRRYKTUUK",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189801292,
                            "md5Sum": "",
                            "nrOfRegions": 6,
                            "nrOfTranscribedRegions": 6,
                            "nrOfWordsInRegions": 136,
                            "nrOfLines": 45,
                            "nrOfTranscribedLines": 45,
                            "nrOfWordsInLines": 175,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381371,
                            "parentTsId": -1,
                            "key": "RJOARZHSGZCFEFAVYTFINPAU",
                            "pageId": 241866,
                            "docId": 7750,
                            "pageNr": 9,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=RJOARZHSGZCFEFAVYTFINPAU",
                            "status": "NEW",
                            "userName": "herve.dejean@xrce.xerox.com",
                            "userId": 275,
                            "timestamp": 1478161451242,
                            "md5Sum": "",
                            "nrOfRegions": 6,
                            "nrOfTranscribedRegions": 6,
                            "nrOfWordsInRegions": 136,
                            "nrOfLines": 45,
                            "nrOfTranscribedLines": 45,
                            "nrOfWordsInLines": 175,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        }
                    ]
                },
                "width": 1115,
                "height": 3496,
                "created": "2016-11-03T09:24:25.936+01:00",
                "indexed": true
            },
            {
                "pageId": 241867,
                "docId": 7750,
                "pageNr": 10,
                "key": "RMINOFMIZIAZJXPHWZFCYAZK",
                "imageId": 227143,
                "url": "https://dbis-thure.uibk.ac.at/f/Get?id=RMINOFMIZIAZJXPHWZFCYAZK&fileType=view",
                "thumbUrl": "https://dbis-thure.uibk.ac.at/f/Get?id=RMINOFMIZIAZJXPHWZFCYAZK&fileType=thumb",
                "imgFileName": "MM_1_005_010.jpg",
                "tsList": {
                    "transcripts": [
                        {
                            "tsId": 382141,
                            "parentTsId": 382130,
                            "key": "SAURDRXKWNGRPSKRRZYZMOWY",
                            "pageId": 241867,
                            "docId": 7750,
                            "pageNr": 10,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=SAURDRXKWNGRPSKRRZYZMOWY",
                            "status": "GT",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478190159382,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 146,
                            "nrOfLines": 57,
                            "nrOfTranscribedLines": 57,
                            "nrOfWordsInLines": 196,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 382130,
                            "parentTsId": 381372,
                            "key": "GLQFSBSTTJLMKKEAZJMOOATF",
                            "pageId": 241867,
                            "docId": 7750,
                            "pageNr": 10,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=GLQFSBSTTJLMKKEAZJMOOATF",
                            "status": "NEW",
                            "userName": "jean-luc.meunier@xrce.xerox.com",
                            "userId": 3556,
                            "timestamp": 1478189824587,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 146,
                            "nrOfLines": 57,
                            "nrOfTranscribedLines": 57,
                            "nrOfWordsInLines": 196,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        },
                        {
                            "tsId": 381372,
                            "parentTsId": -1,
                            "key": "PYPTZNSSPHIPJSPAITXBGNKR",
                            "pageId": 241867,
                            "docId": 7750,
                            "pageNr": 10,
                            "url": "https://dbis-thure.uibk.ac.at/f/Get?id=PYPTZNSSPHIPJSPAITXBGNKR",
                            "status": "NEW",
                            "userName": "herve.dejean@xrce.xerox.com",
                            "userId": 275,
                            "timestamp": 1478161451242,
                            "md5Sum": "",
                            "nrOfRegions": 7,
                            "nrOfTranscribedRegions": 7,
                            "nrOfWordsInRegions": 146,
                            "nrOfLines": 57,
                            "nrOfTranscribedLines": 57,
                            "nrOfWordsInLines": 196,
                            "nrOfWords": 0,
                            "nrOfTranscribedWords": 0
                        }
                    ]
                },
                "width": 1115,
                "height": 3485,
                "created": "2016-11-03T09:24:27.696+01:00",
                "indexed": true
            }
        ]
    },
    "collection": {
        "colId": 3571,
        "colName": "READDU",
        "description": "created by herve.dejean@xrce.xerox.com"
    },
    "edDeclList": []
}


PYTHONIC DATA
{u'md': {u'nrOfPages': 10, u'status': 0
, u'collectionList': {u'colList': [{u'colId': 3571, u'colName': u'READDU', u'description': u'created by herve.dejean@xrce.xerox.com'}]}
, u'scriptType': u'HANDWRITTEN'
, u'docId': 7750
, u'title': u'MM_1_005'
, u'fimgStoreColl': u'TrpDoc_DEA_7750'
, u'createdToTimestamp': 0
, u'createdFromTimestamp': 0
, u'uploader': u'herve.dejean@xrce.xerox.com'
, u'uploaderId': 275
, u'uploadTimestamp': 1478161451242L}
, u'edDeclList': []
, u'collection': {u'colId': 3571, u'colName': u'READDU', u'description': u'created by herve.dejean@xrce.xerox.com'}
, u'pageList': 
    {u'pages': [{u'thumbUrl': u'https://dbis-thure.uibk.ac.at/f/Get?id=DJVKXRYFHSVIDXQXIQIDYEII&fileType=thumb'
                , u'docId': 7750
                , u'created': u'2016-11-03T09:24:11.649+01:00'
                , u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=DJVKXRYFHSVIDXQXIQIDYEII&fileType=view'
                , u'imageId': 227134
                , u'height': 3505
                , u'width': 1079
                , u'imgFileName': u'MM_1_005_001.jpg'
                , u'key': u'DJVKXRYFHSVIDXQXIQIDYEII'
                , u'indexed': True
                , u'pageId': 241858
                , u'pageNr': 1
                , u'tsList': {u'transcripts': [
                    {u'status': u'GT', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381511, u'nrOfTranscribedRegions': 5, u'docId': 7750, u'nrOfLines': 59, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=FDQJTHVXETZGWOTJERYTXTQF', u'userId': 3556, u'md5Sum': u'', u'tsId': 381516, u'nrOfWordsInLines': 217, u'nrOfTranscribedLines': 59, u'nrOfWords': 0, u'key': u'FDQJTHVXETZGWOTJERYTXTQF', u'timestamp': 1478165176495L, u'nrOfWordsInRegions': 163, u'pageId': 241858, u'pageNr': 1, u'nrOfRegions': 5}
                   , {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381509, u'nrOfTranscribedRegions': 5, u'docId': 7750, u'nrOfLines': 59, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=IEDZSBGJXDDXTNJUUQBYTAOE', u'userId': 3556, u'md5Sum': u'', u'tsId': 381511, u'nrOfWordsInLines': 217, u'nrOfTranscribedLines': 59, u'nrOfWords': 0, u'key': u'IEDZSBGJXDDXTNJUUQBYTAOE', u'timestamp': 1478165121979L, u'nrOfWordsInRegions': 163, u'pageId': 241858, u'pageNr': 1, u'nrOfRegions': 5}
                   , {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381506, u'nrOfTranscribedRegions': 5, u'docId': 7750, u'nrOfLines': 59, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=NOHPHKSASMUXUUZADVNFTJWY', u'userId': 3556, u'md5Sum': u'', u'tsId': 381509, u'nrOfWordsInLines': 217, u'nrOfTranscribedLines': 59, u'nrOfWords': 0, u'key': u'NOHPHKSASMUXUUZADVNFTJWY', u'timestamp': 1478165078290L, u'nrOfWordsInRegions': 163, u'pageId': 241858, u'pageNr': 1, u'nrOfRegions': 5}
                   , {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381363, u'nrOfTranscribedRegions': 5, u'docId': 7750, u'nrOfLines': 59, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=XCJJGBTIWVNHBEAJCSNURLVQ', u'userId': 3556, u'md5Sum': u'', u'tsId': 381506, u'nrOfWordsInLines': 217, u'nrOfTranscribedLines': 59, u'nrOfWords': 0, u'key': u'XCJJGBTIWVNHBEAJCSNURLVQ', u'timestamp': 1478164989861L, u'nrOfWordsInRegions': 163, u'pageId': 241858, u'pageNr': 1, u'nrOfRegions': 5}
                   , {u'status': u'NEW', u'userName': u'herve.dejean@xrce.xerox.com', u'parentTsId': -1, u'nrOfTranscribedRegions': 5, u'docId': 7750, u'nrOfLines': 59, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=FMKDLHJQTWVDQOAQBEYMBODW', u'userId': 275, u'md5Sum': u'', u'tsId': 381363, u'nrOfWordsInLines': 217, u'nrOfTranscribedLines': 59, u'nrOfWords': 0, u'key': u'FMKDLHJQTWVDQOAQBEYMBODW', u'timestamp': 1478161451242L, u'nrOfWordsInRegions': 163, u'pageId': 241858, u'pageNr': 1, u'nrOfRegions': 5}
                   ]
                    }
                }
               , {u'thumbUrl': u'https://dbis-thure.uibk.ac.at/f/Get?id=DBFNKQONQBWKKUCODOFAXTXN&fileType=thumb', u'docId': 7750, u'created': u'2016-11-03T09:24:13.43+01:00', u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=DBFNKQONQBWKKUCODOFAXTXN&fileType=view', u'imageId': 227135, u'height': 3513, u'width': 1104, u'imgFileName': u'MM_1_005_002.jpg', u'key': u'DBFNKQONQBWKKUCODOFAXTXN', u'indexed': True, u'pageId': 241859, u'pageNr': 2, u'tsList': {u'transcripts': [{u'status': u'GT', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 382121, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 70, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=OODGHWRQMUWYYMNFCHJJBBDF', u'userId': 3556, u'md5Sum': u'', u'tsId': 382132, u'nrOfWordsInLines': 238, u'nrOfTranscribedLines': 70, u'nrOfWords': 0, u'key': u'OODGHWRQMUWYYMNFCHJJBBDF', u'timestamp': 1478189886242L, u'nrOfWordsInRegions': 175, u'pageId': 241859, u'pageNr': 2, u'nrOfRegions': 7}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 382120, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 70, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=PXZLJGZRNRXRNHHBIQBCTQWW', u'userId': 3556, u'md5Sum': u'', u'tsId': 382121, u'nrOfWordsInLines': 238, u'nrOfTranscribedLines': 70, u'nrOfWords': 0, u'key': u'PXZLJGZRNRXRNHHBIQBCTQWW', u'timestamp': 1478189302829L, u'nrOfWordsInRegions': 175, u'pageId': 241859, u'pageNr': 2, u'nrOfRegions': 7}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381513, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 70, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=SJNLYFZWQDEIESMTDFDKWFEU', u'userId': 3556, u'md5Sum': u'', u'tsId': 382120, u'nrOfWordsInLines': 238, u'nrOfTranscribedLines': 70, u'nrOfWords': 0, u'key': u'SJNLYFZWQDEIESMTDFDKWFEU', u'timestamp': 1478189247739L, u'nrOfWordsInRegions': 175, u'pageId': 241859, u'pageNr': 2, u'nrOfRegions': 7}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381364, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 70, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=IWYPBOPZBTGPZUFHFHUYVIWL', u'userId': 3556, u'md5Sum': u'', u'tsId': 381513, u'nrOfWordsInLines': 238, u'nrOfTranscribedLines': 70, u'nrOfWords': 0, u'key': u'IWYPBOPZBTGPZUFHFHUYVIWL', u'timestamp': 1478165159816L, u'nrOfWordsInRegions': 175, u'pageId': 241859, u'pageNr': 2, u'nrOfRegions': 7}, {u'status': u'NEW', u'userName': u'herve.dejean@xrce.xerox.com', u'parentTsId': -1, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 70, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=XXJNWCMCUINNSHDULAZBQRTS', u'userId': 275, u'md5Sum': u'', u'tsId': 381364, u'nrOfWordsInLines': 238, u'nrOfTranscribedLines': 70, u'nrOfWords': 0, u'key': u'XXJNWCMCUINNSHDULAZBQRTS', u'timestamp': 1478161451242L, u'nrOfWordsInRegions': 175, u'pageId': 241859, u'pageNr': 2, u'nrOfRegions': 7}]}}
               , {u'thumbUrl': u'https://dbis-thure.uibk.ac.at/f/Get?id=UDRRJBUZDRXDFIQRPZKJKSWH&fileType=thumb', u'docId': 7750, u'created': u'2016-11-03T09:24:15.377+01:00', u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=UDRRJBUZDRXDFIQRPZKJKSWH&fileType=view', u'imageId': 227136, u'height': 3501, u'width': 1126, u'imgFileName': u'MM_1_005_003.jpg', u'key': u'UDRRJBUZDRXDFIQRPZKJKSWH', u'indexed': True, u'pageId': 241860, u'pageNr': 3, u'tsList': {u'transcripts': [{u'status': u'GT', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 382123, u'nrOfTranscribedRegions': 6, u'docId': 7750, u'nrOfLines': 60, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=LXDEPITAWFETAMURDTRIEAQL', u'userId': 3556, u'md5Sum': u'', u'tsId': 382133, u'nrOfWordsInLines': 221, u'nrOfTranscribedLines': 60, u'nrOfWords': 0, u'key': u'LXDEPITAWFETAMURDTRIEAQL', u'timestamp': 1478189896358L, u'nrOfWordsInRegions': 167, u'pageId': 241860, u'pageNr': 3, u'nrOfRegions': 6}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381365, u'nrOfTranscribedRegions': 6, u'docId': 7750, u'nrOfLines': 60, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=PPGLFICJMYPQCAZDPMKTDCJX', u'userId': 3556, u'md5Sum': u'', u'tsId': 382123, u'nrOfWordsInLines': 221, u'nrOfTranscribedLines': 60, u'nrOfWords': 0, u'key': u'PPGLFICJMYPQCAZDPMKTDCJX', u'timestamp': 1478189576221L, u'nrOfWordsInRegions': 167, u'pageId': 241860, u'pageNr': 3, u'nrOfRegions': 6}, {u'status': u'NEW', u'userName': u'herve.dejean@xrce.xerox.com', u'parentTsId': -1, u'nrOfTranscribedRegions': 6, u'docId': 7750, u'nrOfLines': 60, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=SKBCTBWMQJJQBZKEQCXOEAXF', u'userId': 275, u'md5Sum': u'', u'tsId': 381365, u'nrOfWordsInLines': 221, u'nrOfTranscribedLines': 60, u'nrOfWords': 0, u'key': u'SKBCTBWMQJJQBZKEQCXOEAXF', u'timestamp': 1478161451242L, u'nrOfWordsInRegions': 167, u'pageId': 241860, u'pageNr': 3, u'nrOfRegions': 6}]}}
               , {u'thumbUrl': u'https://dbis-thure.uibk.ac.at/f/Get?id=YBLJLBUPWCSQVCNAWFYCCLRI&fileType=thumb', u'docId': 7750, u'created': u'2016-11-03T09:24:17.725+01:00', u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=YBLJLBUPWCSQVCNAWFYCCLRI&fileType=view', u'imageId': 227137, u'height': 3518, u'width': 1103, u'imgFileName': u'MM_1_005_004.jpg', u'key': u'YBLJLBUPWCSQVCNAWFYCCLRI', u'indexed': True, u'pageId': 241861, u'pageNr': 4, u'tsList': {u'transcripts': [{u'status': u'GT', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 382124, u'nrOfTranscribedRegions': 5, u'docId': 7750, u'nrOfLines': 45, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=FFQJHLCOMGPWMEAGBVRQRQDY', u'userId': 3556, u'md5Sum': u'', u'tsId': 382134, u'nrOfWordsInLines': 179, u'nrOfTranscribedLines': 45, u'nrOfWords': 0, u'key': u'FFQJHLCOMGPWMEAGBVRQRQDY', u'timestamp': 1478189902824L, u'nrOfWordsInRegions': 139, u'pageId': 241861, u'pageNr': 4, u'nrOfRegions': 5}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381366, u'nrOfTranscribedRegions': 5, u'docId': 7750, u'nrOfLines': 45, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=EVAURZXRDFXCBOEVPEYHJMWQ', u'userId': 3556, u'md5Sum': u'', u'tsId': 382124, u'nrOfWordsInLines': 179, u'nrOfTranscribedLines': 45, u'nrOfWords': 0, u'key': u'EVAURZXRDFXCBOEVPEYHJMWQ', u'timestamp': 1478189629364L, u'nrOfWordsInRegions': 139, u'pageId': 241861, u'pageNr': 4, u'nrOfRegions': 5}, {u'status': u'NEW', u'userName': u'herve.dejean@xrce.xerox.com', u'parentTsId': -1, u'nrOfTranscribedRegions': 5, u'docId': 7750, u'nrOfLines': 45, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=LWVMPOQDBYVZYTEJTYGGUSMJ', u'userId': 275, u'md5Sum': u'', u'tsId': 381366, u'nrOfWordsInLines': 179, u'nrOfTranscribedLines': 45, u'nrOfWords': 0, u'key': u'LWVMPOQDBYVZYTEJTYGGUSMJ', u'timestamp': 1478161451242L, u'nrOfWordsInRegions': 139, u'pageId': 241861, u'pageNr': 4, u'nrOfRegions': 5}]}}
               , {u'thumbUrl': u'https://dbis-thure.uibk.ac.at/f/Get?id=KBKXJPVJZPYRDEVOFEZYWLBV&fileType=thumb', u'docId': 7750, u'created': u'2016-11-03T09:24:19.347+01:00', u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=KBKXJPVJZPYRDEVOFEZYWLBV&fileType=view', u'imageId': 227138, u'height': 3495, u'width': 1109, u'imgFileName': u'MM_1_005_005.jpg', u'key': u'KBKXJPVJZPYRDEVOFEZYWLBV', u'indexed': True, u'pageId': 241862, u'pageNr': 5, u'tsList': {u'transcripts': [{u'status': u'GT', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 382125, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 46, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=RSVUGJANXAOJVCLKWNIHYOOF', u'userId': 3556, u'md5Sum': u'', u'tsId': 382136, u'nrOfWordsInLines': 158, u'nrOfTranscribedLines': 46, u'nrOfWords': 0, u'key': u'RSVUGJANXAOJVCLKWNIHYOOF', u'timestamp': 1478190125606L, u'nrOfWordsInRegions': 119, u'pageId': 241862, u'pageNr': 5, u'nrOfRegions': 7}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381367, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 46, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=GGUZKGAVPNRAPTLODBDJQREM', u'userId': 3556, u'md5Sum': u'', u'tsId': 382125, u'nrOfWordsInLines': 158, u'nrOfTranscribedLines': 46, u'nrOfWords': 0, u'key': u'GGUZKGAVPNRAPTLODBDJQREM', u'timestamp': 1478189670357L, u'nrOfWordsInRegions': 119, u'pageId': 241862, u'pageNr': 5, u'nrOfRegions': 7}, {u'status': u'NEW', u'userName': u'herve.dejean@xrce.xerox.com', u'parentTsId': -1, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 46, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=TKSXYLWVHFQXSSTFNUCHOJZZ', u'userId': 275, u'md5Sum': u'', u'tsId': 381367, u'nrOfWordsInLines': 158, u'nrOfTranscribedLines': 46, u'nrOfWords': 0, u'key': u'TKSXYLWVHFQXSSTFNUCHOJZZ', u'timestamp': 1478161451242L, u'nrOfWordsInRegions': 119, u'pageId': 241862, u'pageNr': 5, u'nrOfRegions': 7}]}}
               , {u'thumbUrl': u'https://dbis-thure.uibk.ac.at/f/Get?id=EXNNKQHSFSZFUSFWHJHSGLFL&fileType=thumb', u'docId': 7750, u'created': u'2016-11-03T09:24:20.817+01:00', u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=EXNNKQHSFSZFUSFWHJHSGLFL&fileType=view', u'imageId': 227139, u'height': 3513, u'width': 1143, u'imgFileName': u'MM_1_005_006.jpg', u'key': u'EXNNKQHSFSZFUSFWHJHSGLFL', u'indexed': True, u'pageId': 241863, u'pageNr': 6, u'tsList': {u'transcripts': [{u'status': u'GT', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 382126, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 58, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=CDIHCQRVKWJQIUFMVKZAZAKZ', u'userId': 3556, u'md5Sum': u'', u'tsId': 382137, u'nrOfWordsInLines': 194, u'nrOfTranscribedLines': 58, u'nrOfWords': 0, u'key': u'CDIHCQRVKWJQIUFMVKZAZAKZ', u'timestamp': 1478190132430L, u'nrOfWordsInRegions': 143, u'pageId': 241863, u'pageNr': 6, u'nrOfRegions': 7}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381368, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 58, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=WLOWSZLXIDSBGNWXNWXDVMDY', u'userId': 3556, u'md5Sum': u'', u'tsId': 382126, u'nrOfWordsInLines': 194, u'nrOfTranscribedLines': 58, u'nrOfWords': 0, u'key': u'WLOWSZLXIDSBGNWXNWXDVMDY', u'timestamp': 1478189729174L, u'nrOfWordsInRegions': 143, u'pageId': 241863, u'pageNr': 6, u'nrOfRegions': 7}, {u'status': u'NEW', u'userName': u'herve.dejean@xrce.xerox.com', u'parentTsId': -1, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 58, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=GIGTEQVBSZUXDVXLGKBMOUIZ', u'userId': 275, u'md5Sum': u'', u'tsId': 381368, u'nrOfWordsInLines': 194, u'nrOfTranscribedLines': 58, u'nrOfWords': 0, u'key': u'GIGTEQVBSZUXDVXLGKBMOUIZ', u'timestamp': 1478161451242L, u'nrOfWordsInRegions': 143, u'pageId': 241863, u'pageNr': 6, u'nrOfRegions': 7}]}}
               , {u'thumbUrl': u'https://dbis-thure.uibk.ac.at/f/Get?id=LPTQSNRVVPFERXFQUZVYJZJT&fileType=thumb', u'docId': 7750, u'created': u'2016-11-03T09:24:22.372+01:00', u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=LPTQSNRVVPFERXFQUZVYJZJT&fileType=view', u'imageId': 227140, u'height': 3479, u'width': 1121, u'imgFileName': u'MM_1_005_007.jpg', u'key': u'LPTQSNRVVPFERXFQUZVYJZJT', u'indexed': True, u'pageId': 241864, u'pageNr': 7, u'tsList': {u'transcripts': [{u'status': u'GT', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 382127, u'nrOfTranscribedRegions': 4, u'docId': 7750, u'nrOfLines': 44, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=AJBVJHMJRZWTBTBTZASIEYON', u'userId': 3556, u'md5Sum': u'', u'tsId': 382138, u'nrOfWordsInLines': 170, u'nrOfTranscribedLines': 44, u'nrOfWords': 0, u'key': u'AJBVJHMJRZWTBTBTZASIEYON', u'timestamp': 1478190139565L, u'nrOfWordsInRegions': 130, u'pageId': 241864, u'pageNr': 7, u'nrOfRegions': 4}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381369, u'nrOfTranscribedRegions': 4, u'docId': 7750, u'nrOfLines': 44, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=PIZEKVZKEQCBESCCICXYXWWC', u'userId': 3556, u'md5Sum': u'', u'tsId': 382127, u'nrOfWordsInLines': 170, u'nrOfTranscribedLines': 44, u'nrOfWords': 0, u'key': u'PIZEKVZKEQCBESCCICXYXWWC', u'timestamp': 1478189755562L, u'nrOfWordsInRegions': 130, u'pageId': 241864, u'pageNr': 7, u'nrOfRegions': 4}, {u'status': u'NEW', u'userName': u'herve.dejean@xrce.xerox.com', u'parentTsId': -1, u'nrOfTranscribedRegions': 4, u'docId': 7750, u'nrOfLines': 44, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=UWMMSHFVNELGGQMFODYGZFIA', u'userId': 275, u'md5Sum': u'', u'tsId': 381369, u'nrOfWordsInLines': 170, u'nrOfTranscribedLines': 44, u'nrOfWords': 0, u'key': u'UWMMSHFVNELGGQMFODYGZFIA', u'timestamp': 1478161451242L, u'nrOfWordsInRegions': 130, u'pageId': 241864, u'pageNr': 7, u'nrOfRegions': 4}]}}
               , {u'thumbUrl': u'https://dbis-thure.uibk.ac.at/f/Get?id=VATMDYPWNWSZKBZYSWLWIXZZ&fileType=thumb', u'docId': 7750, u'created': u'2016-11-03T09:24:24.404+01:00', u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=VATMDYPWNWSZKBZYSWLWIXZZ&fileType=view', u'imageId': 227141, u'height': 3489, u'width': 1125, u'imgFileName': u'MM_1_005_008.jpg', u'key': u'VATMDYPWNWSZKBZYSWLWIXZZ', u'indexed': True, u'pageId': 241865, u'pageNr': 8, u'tsList': {u'transcripts': [{u'status': u'GT', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 382128, u'nrOfTranscribedRegions': 8, u'docId': 7750, u'nrOfLines': 60, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=AIWLPBSWUHABYPSGEPIYBDXY', u'userId': 3556, u'md5Sum': u'', u'tsId': 382139, u'nrOfWordsInLines': 198, u'nrOfTranscribedLines': 60, u'nrOfWords': 0, u'key': u'AIWLPBSWUHABYPSGEPIYBDXY', u'timestamp': 1478190145477L, u'nrOfWordsInRegions': 146, u'pageId': 241865, u'pageNr': 8, u'nrOfRegions': 8}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381370, u'nrOfTranscribedRegions': 8, u'docId': 7750, u'nrOfLines': 60, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=FPSNGGWEVYVHOZXTHEDCZRRS', u'userId': 3556, u'md5Sum': u'', u'tsId': 382128, u'nrOfWordsInLines': 198, u'nrOfTranscribedLines': 60, u'nrOfWords': 0, u'key': u'FPSNGGWEVYVHOZXTHEDCZRRS', u'timestamp': 1478189777858L, u'nrOfWordsInRegions': 146, u'pageId': 241865, u'pageNr': 8, u'nrOfRegions': 8}, {u'status': u'NEW', u'userName': u'herve.dejean@xrce.xerox.com', u'parentTsId': -1, u'nrOfTranscribedRegions': 8, u'docId': 7750, u'nrOfLines': 60, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=COZMHQZMYPYNSQNXDNHONHEI', u'userId': 275, u'md5Sum': u'', u'tsId': 381370, u'nrOfWordsInLines': 198, u'nrOfTranscribedLines': 60, u'nrOfWords': 0, u'key': u'COZMHQZMYPYNSQNXDNHONHEI', u'timestamp': 1478161451242L, u'nrOfWordsInRegions': 146, u'pageId': 241865, u'pageNr': 8, u'nrOfRegions': 8}]}}
               , {u'thumbUrl': u'https://dbis-thure.uibk.ac.at/f/Get?id=CBNMUJLYGDPZFFVLHMWHXATI&fileType=thumb', u'docId': 7750, u'created': u'2016-11-03T09:24:25.936+01:00', u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=CBNMUJLYGDPZFFVLHMWHXATI&fileType=view', u'imageId': 227142, u'height': 3496, u'width': 1115, u'imgFileName': u'MM_1_005_009.jpg', u'key': u'CBNMUJLYGDPZFFVLHMWHXATI', u'indexed': True, u'pageId': 241866, u'pageNr': 9, u'tsList': {u'transcripts': [{u'status': u'GT', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 382129, u'nrOfTranscribedRegions': 6, u'docId': 7750, u'nrOfLines': 45, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=WFCLYZBVQOLRYFDHMUHSAXIB', u'userId': 3556, u'md5Sum': u'', u'tsId': 382140, u'nrOfWordsInLines': 175, u'nrOfTranscribedLines': 45, u'nrOfWords': 0, u'key': u'WFCLYZBVQOLRYFDHMUHSAXIB', u'timestamp': 1478190151621L, u'nrOfWordsInRegions': 136, u'pageId': 241866, u'pageNr': 9, u'nrOfRegions': 6}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381371, u'nrOfTranscribedRegions': 6, u'docId': 7750, u'nrOfLines': 45, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=PSKXONHHRETXTHOZRRYKTUUK', u'userId': 3556, u'md5Sum': u'', u'tsId': 382129, u'nrOfWordsInLines': 175, u'nrOfTranscribedLines': 45, u'nrOfWords': 0, u'key': u'PSKXONHHRETXTHOZRRYKTUUK', u'timestamp': 1478189801292L, u'nrOfWordsInRegions': 136, u'pageId': 241866, u'pageNr': 9, u'nrOfRegions': 6}, {u'status': u'NEW', u'userName': u'herve.dejean@xrce.xerox.com', u'parentTsId': -1, u'nrOfTranscribedRegions': 6, u'docId': 7750, u'nrOfLines': 45, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=RJOARZHSGZCFEFAVYTFINPAU', u'userId': 275, u'md5Sum': u'', u'tsId': 381371, u'nrOfWordsInLines': 175, u'nrOfTranscribedLines': 45, u'nrOfWords': 0, u'key': u'RJOARZHSGZCFEFAVYTFINPAU', u'timestamp': 1478161451242L, u'nrOfWordsInRegions': 136, u'pageId': 241866, u'pageNr': 9, u'nrOfRegions': 6}]}}
               , {u'thumbUrl': u'https://dbis-thure.uibk.ac.at/f/Get?id=RMINOFMIZIAZJXPHWZFCYAZK&fileType=thumb', u'docId': 7750, u'created': u'2016-11-03T09:24:27.696+01:00', u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=RMINOFMIZIAZJXPHWZFCYAZK&fileType=view', u'imageId': 227143, u'height': 3485, u'width': 1115, u'imgFileName': u'MM_1_005_010.jpg', u'key': u'RMINOFMIZIAZJXPHWZFCYAZK', u'indexed': True, u'pageId': 241867, u'pageNr': 10, u'tsList': {u'transcripts': [{u'status': u'GT', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 382130, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 57, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=SAURDRXKWNGRPSKRRZYZMOWY', u'userId': 3556, u'md5Sum': u'', u'tsId': 382141, u'nrOfWordsInLines': 196, u'nrOfTranscribedLines': 57, u'nrOfWords': 0, u'key': u'SAURDRXKWNGRPSKRRZYZMOWY', u'timestamp': 1478190159382L, u'nrOfWordsInRegions': 146, u'pageId': 241867, u'pageNr': 10, u'nrOfRegions': 7}, {u'status': u'NEW', u'userName': u'jean-luc.meunier@xrce.xerox.com', u'parentTsId': 381372, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 57, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=GLQFSBSTTJLMKKEAZJMOOATF', u'userId': 3556, u'md5Sum': u'', u'tsId': 382130, u'nrOfWordsInLines': 196, u'nrOfTranscribedLines': 57, u'nrOfWords': 0, u'key': u'GLQFSBSTTJLMKKEAZJMOOATF', u'timestamp': 1478189824587L, u'nrOfWordsInRegions': 146, u'pageId': 241867, u'pageNr': 10, u'nrOfRegions': 7}, {u'status': u'NEW', u'userName': u'herve.dejean@xrce.xerox.com', u'parentTsId': -1, u'nrOfTranscribedRegions': 7, u'docId': 7750, u'nrOfLines': 57, u'nrOfTranscribedWords': 0, u'url': u'https://dbis-thure.uibk.ac.at/f/Get?id=PYPTZNSSPHIPJSPAITXBGNKR', u'userId': 275, u'md5Sum': u'', u'tsId': 381372, u'nrOfWordsInLines': 196, u'nrOfTranscribedLines': 57, u'nrOfWords': 0, u'key': u'PYPTZNSSPHIPJSPAITXBGNKR', u'timestamp': 1478161451242L, u'nrOfWordsInRegions': 146, u'pageId': 241867, u'pageNr': 10, u'nrOfRegions': 7}]}}
               ]
    }
}

"""


