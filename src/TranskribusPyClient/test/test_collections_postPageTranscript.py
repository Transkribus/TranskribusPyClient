# -*- coding: utf-8 -*-

#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os
import logging

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname((os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) ))) ))
    import TranskribusPyClient_version


from TranskribusPyClient.test import _colId_A, _docId_b
from TranskribusPyClient.client import TranskribusClient, getStoredCredentials

login, pwd = getStoredCredentials()

conn = TranskribusClient(proxies={'https':'http://cornillon:8000'}
                         , loggingLevel=logging.INFO)
print conn

#print conn.auth_logout()

sessionID = conn.auth_login(login, pwd)
print sessionID

#sessionID = conn.auth_login("jean-luc.meunier@xrce.xerox.com", "trnjluc", sHttpsProxyUrl='http://cornillon:8000')


sXml = u"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15/pagecontent.xsd">
    <Metadata>
        <Creator>TRP</Creator>
        <Created>2016-08-18T13:35:08.767+07:00</Created>
        <LastChange>2016-12-01T09:59:24.254+01:00</LastChange>
    </Metadata>
    <Page imageFilename="MM_1_001_005.jpg" imageWidth="1299" imageHeight="3578">
        <ReadingOrder>
            <OrderedGroup id="ro_1480582760956" caption="Regions reading order">
                <RegionRefIndexed index="0" regionRef="region_1471506681127_115"/>
                <RegionRefIndexed index="1" regionRef="region_1471506682080_116"/>
                <RegionRefIndexed index="2" regionRef="region_1471506689643_117"/>
                <RegionRefIndexed index="3" regionRef="region_1480582746513_9"/>
            </OrderedGroup>
        </ReadingOrder>
        <TextRegion type="header" id="region_1471506681127_115" custom="readingOrder {index:0;} structure {type:header;}">
            <Coords points="649,55 896,55 896,143 649,143"/>
            <TextLine id="line_1471506710830_119" custom="readingOrder {index:0;}">
                <Coords points="663,75 872,83 871,118 662,110"/>
                <Baseline points="662,105 871,113"/>
                <TextEquiv>
                    <Unicode>25ten Aprils</Unicode>
                </TextEquiv>
            </TextLine>
            <TextEquiv>
                <Unicode>25ten Aprils</Unicode>
            </TextEquiv>
        </TextRegion>
        <TextRegion type="page-number" id="region_1471506682080_116" custom="readingOrder {index:1;} structure {type:page-number;}">
            <Coords points="988,64 1076,64 1076,130 988,130"/>
            <TextLine id="line_1471506709080_118" custom="readingOrder {index:0;}">
                <Coords points="999,78 1067,80 1066,115 998,113"/>
                <Baseline points="998,108 1066,110"/>
                <TextEquiv>
                    <Unicode>5.</Unicode>
                </TextEquiv>
            </TextLine>
            <TextEquiv>
                <Unicode>5.</Unicode>
            </TextEquiv>
        </TextRegion>
        <TextRegion id="region_1471506689643_117" custom="readingOrder {index:2;}">
            <Coords points="266,151 1054,151 1070,824 1040,3192 910,3186 266,3221"/>
            <TextLine id="line_1471506713518_120" custom="readingOrder {index:0;}">
                <Coords points="342,186 1042,205 1041,240 341,221"/>
                <Baseline points="341,216 1041,235"/>
                <TextEquiv>
                    <Unicode>nen und des Eigenthums ver¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506715830_121" custom="readingOrder {index:1;}">
                <Coords points="343,261 782,273 1057,279 1056,314 781,308 342,296"/>
                <Baseline points="342,291 781,303 1056,309"/>
                <TextEquiv>
                    <Unicode>sprechen, wobey die Munizipa¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506718737_122" custom="readingOrder {index:2;}">
                <Coords points="340,336 746,353 1044,356 1044,391 745,388 339,371"/>
                <Baseline points="339,366 745,383 1044,386"/>
                <TextEquiv>
                    <Unicode>lität die Anzeige von den zu</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506721768_123" custom="readingOrder {index:3;}">
                <Coords points="349,419 724,432 1053,443 1052,478 723,467 348,454"/>
                <Baseline points="348,449 723,462 1052,473"/>
                <TextEquiv>
                    <Unicode>diesem Ende hin von ihr getrof¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506724268_124" custom="readingOrder {index:4;}">
                <Coords points="347,494 831,514 1043,524 1042,559 830,549 346,529"/>
                <Baseline points="346,524 830,544 1042,554"/>
                <TextEquiv>
                    <Unicode>fenen Polizey-Anordnungen</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506726956_125" custom="readingOrder {index:5;}">
                <Coords points="338,579 860,596 1037,600 1036,635 859,631 337,614"/>
                <Baseline points="337,609 859,626 1036,630"/>
                <TextEquiv>
                    <Unicode>beyfügt, – findet nun der</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506730315_126" custom="readingOrder {index:6;}">
                <Coords points="333,664 736,679 1041,681 1041,716 735,714 332,699"/>
                <Baseline points="332,694 735,709 1041,711"/>
                <TextEquiv>
                    <Unicode>kleine Rath kein Bedenken,</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506733378_127" custom="readingOrder {index:7;}">
                <Coords points="336,731 823,750 1047,761 1046,796 822,785 335,766"/>
                <Baseline points="335,761 822,780 1046,791"/>
                <TextEquiv>
                    <Unicode>bey dem fränkischen Generalen</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506736549_128" custom="readingOrder {index:8;}">
                <Coords points="339,822 864,839 1051,848 1050,883 863,874 338,857"/>
                <Baseline points="335,852 860,869 1047,878"/>
                <TextEquiv>
                    <Unicode>Seras (lt. Mißiven) um Wegzie¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506747393_129" custom="readingOrder {index:9;}">
                <Coords points="332,895 811,906 1055,915 1054,950 810,941 331,930"/>
                <Baseline points="331,925 810,936 1054,945"/>
                <TextEquiv>
                    <Unicode>hung der in die Gemeinde Hirzel¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506750659_130" custom="readingOrder {index:10;}">
                <Coords points="338,971 826,982 1058,987 1057,1022 825,1017 337,1006"/>
                <Baseline points="337,1001 825,1012 1057,1017"/>
                <TextEquiv>
                    <Unicode>detaschirten Truppen anzusu¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506753003_131" custom="readingOrder {index:11;}">
                <Coords points="339,1053 1055,1069 1054,1104 338,1088"/>
                <Baseline points="338,1083 1054,1099"/>
                <TextEquiv>
                    <Unicode>chen, ertheilt aber dem Herrn</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506755847_132" custom="readingOrder {index:12;}">
                <Coords points="327,1127 860,1139 1066,1144 1065,1179 859,1174 326,1162"/>
                <Baseline points="326,1157 859,1169 1065,1174"/>
                <TextEquiv>
                    <Unicode>Adjunct Dr. Landis zu Richter¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506758972_133" custom="readingOrder {index:13;}">
                <Coords points="333,1194 850,1211 1071,1214 1071,1249 849,1246 332,1229"/>
                <Baseline points="332,1224 849,1241 1071,1244"/>
                <TextEquiv>
                    <Unicode>schweil, unter dießfälliger An¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506761440_134" custom="readingOrder {index:14;}">
                <Coords points="320,1269 1065,1289 1064,1324 319,1304"/>
                <Baseline points="319,1299 1064,1319"/>
                <TextEquiv>
                    <Unicode>zeige, den Auftrag, die Munici</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506764112_135" custom="readingOrder {index:15;}">
                <Coords points="333,1352 788,1361 1059,1372 1058,1407 787,1396 332,1387"/>
                <Baseline points="332,1382 787,1391 1058,1402"/>
                <TextEquiv>
                    <Unicode>palität im Hirzel bey Eröffnung</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506766815_136" custom="readingOrder {index:16;}">
                <Coords points="337,1432 931,1447 1053,1450 1052,1485 930,1482 336,1467"/>
                <Baseline points="336,1462 930,1477 1052,1480"/>
                <TextEquiv>
                    <Unicode>gegenwärtiger Verfügung zu</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506769472_137" custom="readingOrder {index:17;}">
                <Coords points="323,1515 673,1523 1035,1529 1035,1564 672,1558 322,1550"/>
                <Baseline points="322,1545 672,1553 1035,1559"/>
                <TextEquiv>
                    <Unicode>ihren eigenen Handen und zu</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506772566_138" custom="readingOrder {index:18;}">
                <Coords points="329,1594 843,1605 1056,1609 1055,1644 842,1640 328,1629"/>
                <Baseline points="328,1624 842,1635 1055,1639"/>
                <TextEquiv>
                    <Unicode>Handen aller Bürger, welche die</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506775628_139" custom="readingOrder {index:19;}">
                <Coords points="321,1676 867,1684 1059,1690 1058,1725 866,1719 321,1711"/>
                <Baseline points="321,1706 866,1714 1058,1720"/>
                <TextEquiv>
                    <Unicode>gedachten Verpflichtungen mit</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506777909_140" custom="readingOrder {index:20;}">
                <Coords points="312,1758 1028,1769 1028,1804 312,1793"/>
                <Baseline points="312,1788 1028,1799"/>
                <TextEquiv>
                    <Unicode>ihrer Unterschrift bekräftigt</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506780644_141" custom="readingOrder {index:21;}">
                <Coords points="326,1830 940,1849 1054,1857 1052,1892 938,1884 325,1865"/>
                <Baseline points="325,1860 938,1879 1052,1887"/>
                <TextEquiv>
                    <Unicode>haben, ernstlich aufzufordern,</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506783394_142" custom="readingOrder {index:22;}">
                <Coords points="322,1913 679,1918 1051,1928 1050,1963 678,1953 322,1948"/>
                <Baseline points="322,1943 678,1948 1050,1958"/>
                <TextEquiv>
                    <Unicode>dieselben von nun an immer auf</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506785988_143" custom="readingOrder {index:23;}">
                <Coords points="322,1992 607,1995 1012,2014 1011,2049 606,2030 322,2027"/>
                <Baseline points="322,2022 606,2025 1011,2044"/>
                <TextEquiv>
                    <Unicode>das pünktlichste zu erfüllen,</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506788847_144" custom="readingOrder {index:24;}">
                <Coords points="304,2079 762,2086 1048,2089 1048,2124 762,2121 304,2114"/>
                <Baseline points="304,2109 762,2116 1048,2119"/>
                <TextEquiv>
                    <Unicode>maßen bey eintrettendem un¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506791706_145" custom="readingOrder {index:25;}">
                <Coords points="324,2155 840,2166 1048,2171 1047,2206 839,2201 323,2190"/>
                <Baseline points="323,2185 839,2196 1047,2201"/>
                <TextEquiv>
                    <Unicode>verhofftem Fall wiederholter</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506794347_146" custom="readingOrder {index:26;}">
                <Coords points="316,2233 904,2253 1034,2257 1033,2292 903,2288 315,2268"/>
                <Baseline points="315,2263 903,2283 1033,2287"/>
                <TextEquiv>
                    <Unicode>Vergehungen gegen die öffentliche</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506797753_147" custom="readingOrder {index:27;}">
                <Coords points="309,2318 758,2331 1053,2336 1052,2371 757,2366 308,2353"/>
                <Baseline points="308,2348 757,2361 1052,2366"/>
                <TextEquiv>
                    <Unicode>Ruhe und Sicherheit oder Be¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506800832_148" custom="readingOrder {index:28;}">
                <Coords points="321,2404 848,2404 1017,2414 1052,2428 1038,2461 1009,2448 847,2439 321,2439"/>
                <Baseline points="321,2434 847,2434 1010,2443 1040,2456"/>
                <TextEquiv>
                    <Unicode>einträchtigung einzelner Bürger,</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506803582_149" custom="readingOrder {index:29;}">
                <Coords points="309,2482 790,2488 1017,2485 1017,2520 790,2523 309,2517"/>
                <Baseline points="309,2512 790,2518 1017,2515"/>
                <TextEquiv>
                    <Unicode>die Regierung ernstlichere</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506811972_150" custom="readingOrder {index:30;}">
                <Coords points="308,2554 913,2564 1038,2566 1038,2601 913,2599 308,2589"/>
                <Baseline points="308,2584 913,2594 1038,2596"/>
                <TextEquiv>
                    <Unicode>Maßregeln zu ergreifen genöth¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506814691_151" custom="readingOrder {index:31;}">
                <Coords points="310,2635 718,2641 1030,2649 1029,2684 717,2676 310,2670"/>
                <Baseline points="310,2665 717,2671 1029,2679"/>
                <TextEquiv>
                    <Unicode>iget wäre. Übrigens soll durch</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506817535_152" custom="readingOrder {index:32;}">
                <Coords points="299,2725 736,2727 1031,2724 1031,2759 736,2762 299,2760"/>
                <Baseline points="299,2755 736,2757 1031,2754"/>
                <TextEquiv>
                    <Unicode>diese Verfügung der Fortgang</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506820019_153" custom="readingOrder {index:33;}">
                <Coords points="316,2796 1022,2801 1022,2836 316,2831"/>
                <Baseline points="316,2826 1022,2831"/>
                <TextEquiv>
                    <Unicode>des gegen den Jacob Schärer und</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506822957_154" custom="readingOrder {index:34;}">
                <Coords points="306,2880 822,2883 1027,2887 1026,2922 822,2918 306,2915"/>
                <Baseline points="306,2910 822,2913 1026,2917"/>
                <TextEquiv>
                    <Unicode>allfällig andre, gleicher Verge¬</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506826129_155" custom="readingOrder {index:35;}">
                <Coords points="306,2966 831,2972 969,2968 1051,2991 1042,3025 964,3003 831,3007 306,3001"/>
                <Baseline points="306,2996 831,3002 965,2998 1043,3020"/>
                <TextEquiv>
                    <Unicode>hungen wegen aggravierte Per</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506829066_156" custom="readingOrder {index:36;}">
                <Coords points="293,3055 625,3053 1031,3056 1031,3091 625,3088 293,3090"/>
                <Baseline points="293,3085 625,3083 1031,3086"/>
                <TextEquiv>
                    <Unicode>sonen, in keinen Theilen gehemmt</Unicode>
                </TextEquiv>
            </TextLine>
            <TextLine id="line_1471506831691_157" custom="readingOrder {index:37;}">
                <Coords points="301,3131 722,3128 1006,3126 1006,3161 722,3163 301,3166"/>
                <Baseline points="301,3161 722,3158 1006,3156"/>
                <TextEquiv>
                    <Unicode>seyn. Dieser Beschluß wird auch</Unicode>
                </TextEquiv>
            </TextLine>
            <TextEquiv>
                <Unicode>nen und des Eigenthums ver¬
sprechen, wobey die Munizipa¬
lität die Anzeige von den zu
diesem Ende hin von ihr getrof¬
fenen Polizey-Anordnungen
beyfügt, – findet nun der
kleine Rath kein Bedenken,
bey dem fränkischen Generalen
Seras (lt. Mißiven) um Wegzie¬
hung der in die Gemeinde Hirzel¬
detaschirten Truppen anzusu¬
chen, ertheilt aber dem Herrn
Adjunct Dr. Landis zu Richter¬
schweil, unter dießfälliger An¬
zeige, den Auftrag, die Munici
palität im Hirzel bey Eröffnung
gegenwärtiger Verfügung zu
ihren eigenen Handen und zu
Handen aller Bürger, welche die
gedachten Verpflichtungen mit
ihrer Unterschrift bekräftigt
haben, ernstlich aufzufordern,
dieselben von nun an immer auf
das pünktlichste zu erfüllen,
maßen bey eintrettendem un¬
verhofftem Fall wiederholter
Vergehungen gegen die öffentliche
Ruhe und Sicherheit oder Be¬
einträchtigung einzelner Bürger,
die Regierung ernstlichere
Maßregeln zu ergreifen genöth¬
iget wäre. Übrigens soll durch
diese Verfügung der Fortgang
des gegen den Jacob Schärer und
allfällig andre, gleicher Verge¬
hungen wegen aggravierte Per
sonen, in keinen Theilen gehemmt
seyn. Dieser Beschluß wird auch</Unicode>
            </TextEquiv>
        </TextRegion>
        <TextRegion type="catch-word" id="region_1480582746513_9" custom="readingOrder {index:3;} structure {type:catch-word;}">
            <Coords points="850,3214 984,3214 984,3283 850,3283"/>
            <TextLine id="line_1480582752832_10" custom="readingOrder {index:0;}">
                <Coords points="858,3221 966,3219 967,3269 859,3271"/>
                <Baseline points="859,3266 967,3264"/>
                <TextEquiv>
                    <Unicode></Unicode>
                </TextEquiv>
            </TextLine>
            <TextEquiv>
                <Unicode></Unicode>
            </TextEquiv>
        </TextRegion>
    </Page>
</PcGts>

"""
import types
assert type(sXml) == types.UnicodeType
# ret = conn.getDocumentFromServer(colid, docid)
#ret = conn.getDocumentFromServer("3571", "7750")
#data = conn.collections_postPageTranscript(3989, 8255, 1, "New", sXml, sNote="test by JL")
data = conn.collections_postPageTranscript(3989, 8255, 1, sXml)
print data


conn.setProxies({'https':'http://cornillon:8000'})

print conn.auth_logout()

"""
<?xml version="1.0" encoding="UTF-8" standalone="yes"?><trpTranscriptMetadata><tsId>424778</tsId><parentTsId>-1</parentTsId><key>IXQDKIMHCKSJAAVUZLWMIKRV</key><pageId>252384</pageId><docId>8255</docId><pageNr>1</pageNr><url>https://dbis-thure.uibk.ac.at/f/Get?id=IXQDKIMHCKSJAAVUZLWMIKRV</url><status>IN_PROGRESS</status><userName>jean-luc.meunier@xrce.xerox.com</userName><userId>3556</userId><timestamp>1481281786096</timestamp><md5Sum></md5Sum><nrOfRegions>4</nrOfRegions><nrOfTranscribedRegions>3</nrOfTranscribedRegions><nrOfWordsInRegions>131</nrOfWordsInRegions><nrOfLines>41</nrOfLines><nrOfTranscribedLines>40</nrOfTranscribedLines><nrOfWordsInLines>168</nrOfWordsInLines><nrOfWords>0</nrOfWords><nrOfTranscribedWords>0</nrOfTranscribedWords></trpTranscriptMetadata>

<trpTranscriptMetadata>
    <tsId>424778</tsId>
    <parentTsId>-1</parentTsId>
    <key>IXQDKIMHCKSJAAVUZLWMIKRV</key>
    <pageId>252384</pageId>
    <docId>8255</docId>
    <pageNr>1</pageNr>
    <url>https://dbis-thure.uibk.ac.at/f/Get?id=IXQDKIMHCKSJAAVUZLWMIKRV</url>
    <status>IN_PROGRESS</status>
    <userName>jean-luc.meunier@xrce.xerox.com</userName>
    <userId>3556</userId>
    <timestamp>1481281786096</timestamp>
    <md5Sum/>
    <nrOfRegions>4</nrOfRegions>
    <nrOfTranscribedRegions>3</nrOfTranscribedRegions>
    <nrOfWordsInRegions>131</nrOfWordsInRegions>
    <nrOfLines>41</nrOfLines>
    <nrOfTranscribedLines>40</nrOfTranscribedLines>
    <nrOfWordsInLines>168</nrOfWordsInLines>
    <nrOfWords>0</nrOfWords>
    <nrOfTranscribedWords>0</nrOfTranscribedWords>
</trpTranscriptMetadata>
"""


