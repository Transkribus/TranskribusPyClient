#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    Dealing with transcripts
    
    JL Meunier - September 2017

    Copyright Naver(C) 2017 JL. Meunier

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

#    TranskribusCommands/do_LAbatch.py 3571 3820 8251 8252


#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os, logging
from optparse import OptionParser
import json

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit
from TranskribusPyClient.client import TranskribusClient
from TranskribusPyClient.PageRangeSpec import PageRangeSpec
from TranskribusPyClient.TimeRangeSpec import DateTimeRangeSpec
from TranskribusPyClient.TRP_FullDoc import TRP_FullDoc

from common.trace import traceln, trace

DEBUG = 0

description = """Managiong the transcripts of one or several document(s) or of a whole collection.
""" + _Trnskrbs_description

usage = """%s <colId> <docId> [<page-ranges>] [--within <date>/<date>]+ [--at <date>]+ [--after <date>] [--before <date>] [--utc] [--check_user <username>] <operation>

To filter the transcripts before applying the operation, use:
 page ranges
 --at, --within, --after, --before for time filtering
 
To check assumption regarding the transcripts before applying the operation, use:
 --check_user, --check_status

<operation> is one of:
--list    list the in-scope transcripts  (default operation if none given)
--rm      REMOVE the in-scope transcripts

Page range is a comma-separated series of integer or pair of integers separated by a '-' 
For instance 1  or 1,3  or 1-4 or 1,3-6,8

Date takes the form: 
        YYYY-MM-DDThh:mm:ss+HHMM  like 2017-09-04T18:30:20+0100 
        YYYY-MM-DDThh:mm:ss-HHMM  like 2017-09-04T18:30:20-0100 
        YYYY-MM-DDThh:mm:ssZ  like 2017-09-04T18:30:20Z 
    Incomplete dates are converted into the first millisecond of the given period. For instance 2017 is equivalent to 2017-01-01T00:00:00
Alternatively, it can be a timestamp (number of milliseconds since 1970-01-01)
--utc option will show UTC times

User name are regular expression (as specified in Python re library)

"""%sys.argv[0]

class DoTranscript(TranskribusClient):
    sDefaultServerUrl = _Trnskrbs_default_url
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
    
    def filter(self, colId, docId, page_filter=None, time_filter=None, bVerbose=False):
        trp = TRP_FullDoc(self.getDocById(colId, docId, -1))
    
        if page_filter:
            if bVerbose: 
                trace("\t[filter] as per page specification: %s"%page_filter)
                n0 = len(trp.getPageList())
            trp.filterPageList(page_filter)
            if bVerbose: 
                n1 = len(trp.getPageList())
                traceln(" --> %d pages in-scope (after excluding %d)"%(n1, n0-n1))
        
        if time_filter:
            if bVerbose: 
                trace("\t[filter] as per time specification: %s"%time_filter)
                n0 = len(trp.getTranscriptList())
            trp.filterTranscriptsByTime(time_filter)
            if bVerbose: 
                n1 = len(trp.getTranscriptList())
                traceln(" --> %d transcripts in-scope (after excluding %d)"%(n1, n0-n1))
        return trp
    
    @classmethod
    def _checkAsSet(cls, lV, lVref):
        """
        compare those 
        """
    def check(self, trp, user_check=None, status_check=None, bVerbose=False):
        """
        Check those conditions, and raises a ValueError if some condition is not met
        return True
        """
        if user_check:
            if bVerbose: traceln("\t[check] required user(s): %s"%user_check)
            lUser = trp.getTranscriptUsernameList()
            if not set(user_check).issuperset(set(lUser)):
                if bVerbose:
                    lExtra = list(set(lUser).difference(set(user_check)))
                    lExtra.sort()
                    traceln("\tERROR: selected transcript include those usernames: ", lExtra)
                raise ValueError("Extra user(s) found.")
        
        if status_check:
            if bVerbose: traceln("\t[check] required status(es): %s"%status_check)
            lStatus = trp.getTranscriptStatusList()
            if not set(status_check).issuperset(set(lStatus)):
                if bVerbose:
                    lExtra = list(set(lStatus).difference(set(status_check)))
                    lExtra.sort()
                    traceln("\tERROR: selected transcript include those status(es): ", lExtra)
                raise ValueError("Extra status(es) found.")

        return True
    
    def deleteTranscripts(self, trp, bVerbose=True):
        """
        Delete the transcripts listed in the trp
        """
        colId = trp.getCollectionId()
        ldTr = trp.getTranscriptList()
        
        for dTr in ldTr:
            docId = dTr["docId"]
            pnum = dTr["pageNr"]
            sKey = dTr["key"]
            if bVerbose:
                traceln("\tdeleting %s %s p%s transcript %s"%(colId, docId, pnum, sKey))
                traceln(self.deletePageTranscript(colId, docId, pnum, sKey))

if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoTranscript.sDefaultServerUrl)
    parser.add_option("--after" , dest='after' , action="store", type="string", default=None, help="Consider transcripts created on or after this date.")
    parser.add_option("--before", dest='before', action="store", type="string", default=None, help="Consider transcripts created on or before this date.")
    parser.add_option("--within", dest='within', action="append", type="string", default=None, help="Consider transcripts created within this range(s) of dates.")
    parser.add_option("--at"    , dest='at'    , action="append", type="string", default=None, help="Consider transcripts created at a date(s).")
    parser.add_option("--check_user"  , dest='check_user'   , action="append", type="string", default=None, help="Check that the transcripts were authored by this or these users.")
    parser.add_option("--check_status", dest='check_status' , action="append", type="string", default=None, help="Check that the transcripts have this or these status(es).")
    parser.add_option("-n", "--n"  , dest='nbTranscript', action="store", type="int", default=1, help="Number of transcripts")

    parser.add_option("--utc"   , dest='utc'        , action="store_true", default=False, help="Show UTC time.")
    
    parser.add_option("--list"  , dest='op_list'    , action="store_true", default=False, help="List   the in-scope transcripts.")
    parser.add_option("--rm"    , dest='op_rm'      , action="store_true", default=False, help="Remove the in-scope transcripts. (CAUTION)")
        
    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    doer = DoTranscript(options.server, proxies, loggingLevel=logging.WARN)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)
    # --- 
    try:                        colId = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
    try:                        docId = int(args.pop(0))
    except Exception as e:      _exit(usage, 1, e)
    #docId           = int(args.pop(0)) if args else None
    sPageRangeSpec  = args.pop(0)      if args else None

    if args:                    _exit(usage, 2, Exception("Extra arguments to the command"))

    #PAGE RANGE FILTER
    oPageRange = PageRangeSpec(sPageRangeSpec) if sPageRangeSpec else None
    
    #TIME RANGE FILTER
    if options.utc:  DateTimeRangeSpec.setUTC(True)
    oTimeRange = DateTimeRangeSpec()
    if options.before:
        oTimeRange.addEndsBefore(options.before)
    if options.after:
        oTimeRange.addStartsAfter(options.after)
    if options.within:
        for sA_slash_B in options.within:
            sA, sB = sA_slash_B.split("/")
            oTimeRange.addRange(sA, sB)
    if options.at:
        for sA in options.at:
            oTimeRange.addRange(sA, sA)
    if not oTimeRange: oTimeRange = None
    
    #CHECKs
    lUser   = options.check_user   if options.check_user   else None
    lStatus = options.check_status if options.check_status else None
    
    # --- 
    # get a filtered TRP data
    trp = doer.filter(colId, docId, page_filter=oPageRange, time_filter=oTimeRange, bVerbose=True)

    #CHECKs
    try:
        doer.check(trp, user_check=lUser, status_check=lStatus, bVerbose=True) 
    except ValueError:
        traceln(" --- ERROR ---")
        traceln(trp.report_short(warn="!"))
        traceln("ERROR: some check(s) failed.")
        sys.exit(3)
    
    traceln()
    
    if options.op_rm == True:
        #delete the transcripts remaining in trp !
        doer.deleteTranscripts(trp, bVerbose=True)
    else:
        #by default we list
        print trp.report_short()
        
    traceln()      
    traceln("- Done")
    
