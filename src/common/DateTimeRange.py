# -*- coding: utf-8 -*-

"""
    DateTime range specification for Python clients
    
    A class to deal with date+time or date range specifications like 
        --after 1504512814466    (Transkribus milliseconds timestamp)
        --after 
    
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
import time
import datetime
import dateutil.parser

from common.IntegerRangeHalfBounded import IntegerRangeHalfBounded


class DateTimeRange(IntegerRangeHalfBounded):
    """
    A list of datetime range object
    
    - date time have the form: 2017-09-04 --aft 2017-09-04T14:00         (before the 1st date and after the second one)

    - the object is a container that supports:
        - contains test (if n in o: ...)
    """
#     dt0 = datetime.datetime(1970, 1, 1)
    dt0 = dateutil.parser.parse("1970/01/01T00:00:00+0000")
    ts0 = 0
    
    bUTC = False
    
    def __init__(self):
        IntegerRangeHalfBounded.__init__(self)
        
    @classmethod 
    def setUTC(cls, bUTC):
        cls.bUTC = bUTC
        return bUTC

    def addRange(self, sDateTimeA_or_dt, sDateTimeB_or_dt):
        """
        add a range
        """
        tsA = self.o2ts(sDateTimeA_or_dt)
        tsB = self.o2ts(sDateTimeB_or_dt)
        IntegerRangeHalfBounded.addRange(self, tsA, tsB)
        
        
    def addStartsAfter(self, sDateTimeA_or_dt):
        """
        Start of the interval
        """
        tsA = self.o2ts(sDateTimeA_or_dt)
        IntegerRangeHalfBounded.addRange(self, tsA, self.inf())
       
    def addEndsBefore(self, sDateTimeB_or_dt):
        """
        end of the interval
        """
        tsB = self.o2ts(sDateTimeB_or_dt)
        IntegerRangeHalfBounded.addRange(self, -self.inf(), tsB)
    
    # -------------------------------------------------------------------------------
    @classmethod
    def o2dt(cls, o):
        """
        make a datetime out of this thing
        """
        if isinstance(o, datetime.datetime): return o
        try:
            o+0 #numerical value?
            return cls.ts2dt(o)
        except TypeError:
            if type(o) == types.StringType: return cls.txt2dt(o)  #the timezone should be indicated in the string...
        raise ValueError("Cannot convert to datetime the object '%s'"%`o`)

    @classmethod
    def o2ts(cls, o):
        """
        make a timestamp out of this thing
        """
        try:
            o+0 #numerical value?
            return o
        except TypeError:
            if isinstance(o, datetime.datetime): return cls.dt2ts(o)
            if type(o) == types.StringType:      
                try:
                    return cls.txt2ts(o)
                except ValueError:
                    return cls.dt2ts(cls.txt2dt(o))
        raise ValueError("Cannot convert to timestamp the object '%s'"%`o`)      
      
    # -------------------------------------------------------------------------------
    @classmethod
    def txt2dt(cls, sDateTime):
        """
        convert a string to a datetime
        The string can be a timestamp or a ISO-like textual date, with a t least the year
        return a datetime or raise a ValueError exception
        """
        #first try looking at it as a timestamp
        try:    return cls.ts2dt(sDateTime)
        except: pass
        if len(sDateTime) < 13: raise ValueError("The date and the hour must at least be specified")
        return dateutil.parser.parse(sDateTime)

    @classmethod
    def ts2dt(cls, ts):
        """
        a timestamp here is the number of milliseconds since 1/1/1970
        NOTE: in Python it is the number of seconds! and it is a float
        
        return a DateTime object
        """
#         if ts <= 0: raise ValueError("Negative timestamp")
        if type(ts) == types.StringType:
            ts = long(ts)
        
        if cls.bUTC:
            dt = datetime.datetime.utcfromtimestamp(ts/1000.0)
        else:
            dt = datetime.datetime.fromtimestamp(ts/1000.0) #showing local time
        return dt

    # -------------------------------------------------------------------------------
    @classmethod
    def txt2ts(cls, sTS):
        return long(sTS)
    
    @classmethod
    def dt2ts(cls, dt_or_s):
        """
        get either a datetime object or a textual date that is parsed. (Must be in form: "%Y-%m-%dT%H:%M:%S.%f")
        
        return a timestamp  (number of milliseconds since Thu Jan 01 01:00:00 1970)
        """
        if type(dt_or_s) == types.StringType:
            dt = cls.txt2dt(dt_or_s)
        else:
            dt = dt_or_s
            
        ts = int((dt-cls.dt0).total_seconds() * 1000)
        #assert cls.format(cls.ts2dt(ts)).startswith(sDateTime)

        return ts

    # -------------------------------------------------------------------------------
    @classmethod
    def getTimeZone(cls):
        nbSecWest = time.altzone
        h, m = int(nbSecWest/3600), nbSecWest % 3600
        if h > 0:
            return "-%02d%02d"%( h,m)
        else:
            return "+%02d%02d"%(-h,m)
        
    @classmethod
    def isoformat(cls, dt_or_o):
        """
        similar to  ISO 8601 format, YYYY-MM-DDTHH:MM:SS.mmmmmm
        but with less decimal (so that we show only meaningful and distinguishable ones)
        """   
        if cls.bUTC:
            return cls.o2dt(dt_or_o).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z" #discard the 3 last 0s
        else:
            return cls.o2dt(dt_or_o).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + cls.getTimeZone() #discard the 3 last 0s
        #return cls.o2dt(dt_or_o).isoformat()[:-3] #discard the 3 last 0s  but no timezone!! :-/

    format = isoformat
    
    def __str__(self): 
        
        return ",".join( "%s / %s"%(a,b) if a != b else "{ %s }"%a for (a,b) in [( self.isoformat(a) if a!=-self._fINF else ""
                                                                          ,  self.isoformat(b) if b!=+self._fINF else "") for a,b in self._ltAB] )
    # -------------------------------------------------------------------------------
        
#     def _check(self):
#         """
#         check that the date time interval makes sense
#         """
#         noStart   = None
#         noEnd     = None
#         maxB      = None
#         for a, b in self._ltAB:
#             if noStart and a == None: ValueError("Invalid sequence of interval: multiple ranges without a start")
#             if noEnd:                 ValueError("Invalid sequence of interval: cannot add a range after an open-ended range")
#             if a == None: noStart = True
#             if b == None: noEnd   = True
#             
#             if maxB and a == None: raise ValueError("Invalid sequence of interval: open-start range not at start of sequence")
#                 
#             if self.bInclusive:
#                 if maxB and maxB >= a:    raise ValueError("Invalid sequence of interval: %s >= %s"%(self._str(maxB), self._str(a)))
#             else:
#                 if maxB and maxB > a:    raise ValueError("Invalid sequence of interval: %s > %s"%(self._str(maxB), self._str(a)))
#             if a and b and not self.lt(a, b): raise ValueError("Invalid interval: %s %s %s"%(self._str(a)
#                                                                                             , ">" if self.bInclusive else ">="
#                                                                                             , self._str(b)))
#             maxB = max(maxB, a, b)
#             
    
    
#     @classmethod
#     def parseSpec(cls, sDT):
#         """
#         parse a timedate and return a timestamp float (number of milliseconds since Thu Jan 01 01:00:00 1970)
#         
#         "%Y-%m-%dT%H:%M:%S"
#         """
#         for i in range(6, 0, -1):  #from "%Y-%m-%dT%H:%M:%S"  to "%Y"
#             sFmt = "".join(["%Y", "-%m", "-%d", "T%H", ":%M", ":%S"])
#             try:
#                 ts = datetime.datetime.strptime(sDT, sFmt)
#                 assert sDT == time.strftime(sFmt, time.gmtime(ts))
#             except ValueError:
#                 dt = None
#         if dt == None: raise ValueError("Invalid date or datetime: %s"%sDT)
#         return dt
# 
#     def __contains__(self, sDT):
#         if type(item) != types.IntType: raise ValueError("A page range contains integer values not %s"%type(item))
#         a, b = None, None
#         for a,b in self._ltAB:
#             if b >= item: break
#         return a<= item and item <= b

"""
def test_good_spec(capsys):
    def container_test(o, lref):
        assert list(o) == lref
        assert list(reversed(o)) == list(reversed(lref))
        for item in lref: assert item in o
        assert -99 not in o
        
    o = DateTimeRange("1")
#     with capsys.disabled():
#         print "YOOOOOOOOOOOOOOOOOOOOOOOOOOO ", list(reversed(o))    
    container_test(o, [1])
    
    import pytest
    with pytest.raises(ValueError): DateTimeRange("1 3")
"""


def test_class_methods():
    import pytest

#     assert datetime.datetime(1970, 1, 1) == DateTimeRange.ts2dt(0)
#     assert datetime.datetime(1970, 1, 1) == DateTimeRange.ts2dt("0")
    assert DateTimeRange.ts2dt(10000)
    with pytest.raises(ValueError): DateTimeRange.ts2dt("yo man")
    
    assert DateTimeRange.dt2ts("1970-01-01T00:00:00.000Z") == 0
    assert DateTimeRange.dt2ts("1969-12-31T23:59:00.000Z") == -60000
    with pytest.raises(ValueError): DateTimeRange.ts2dt("yo man")
    
    DateTimeRange.setUTC(True)
    assert DateTimeRange.format(0) == "1970-01-01T00:00:00.000Z"
    assert DateTimeRange.format(datetime.datetime(1970, 1, 1)) == "1970-01-01T00:00:00.000Z"
    
    ts = 1504615116779
    dt = datetime.datetime(2017, 9, 5, 12, 38, 36, 779000)
    assert DateTimeRange.ts2dt(1504615116779) == dt
    
def test_simple():
    import pytest
    dts = DateTimeRange()
    assert dts.len() == 0
    
    dts.addRange("2017-09-04T12:00:00Z", "2017-09-04T23:00:00Z")
    assert dts.len() == (DateTimeRange.dt2ts("2017-09-04T23:00:00Z")-DateTimeRange.dt2ts("2017-09-04T12:00:00Z")+1)
    
    assert DateTimeRange.dt2ts("2017-09-04T12:00:00.000Z") in dts
    assert DateTimeRange.dt2ts("2017-09-04T18:30:20.000Z") in dts
    assert DateTimeRange.dt2ts("2017-09-04T23:00:00.000Z") in dts
    with pytest.raises(ValueError): DateTimeRange.o2ts("2019-09-01")
    with pytest.raises(ValueError): DateTimeRange.o2ts("2010-09") 
    assert DateTimeRange.o2ts("2019-09-01T12Z") not in dts
    
    #with pytest.raises(ValueError): 
    dts.addStartsAfter("2018-01-01T00:00Z")
    assert dts.len() == dts.inf()
    
    def test_1():
        assert DateTimeRange.dt2ts("2019-09-01T00:00Z") in dts
        assert DateTimeRange.dt2ts("2010-01T00:00Z") not in dts
        assert DateTimeRange.dt2ts("2017-12-31T23:59:59Z") not in dts
    test_1()

    with pytest.raises(ValueError): dts.addStartsAfter("2018-01-01")
    with pytest.raises(ValueError): dts.addStartsAfter("2012-01-01")
    with pytest.raises(ValueError): dts.addStartsAfter("2022-01-01")
    test_1()

    dts.addEndsBefore("2000-12-31T23:59:59Z")
    def test_2():
        assert DateTimeRange.dt2ts("1990-10-29T19:00Z") in dts
        assert DateTimeRange.dt2ts("2000-12-31T23:59:59Z") in dts
        assert DateTimeRange.dt2ts("2000-12-31T23:59:58Z") in dts
        assert DateTimeRange.dt2ts("2001-01-01T00:00:00Z") not in dts
    test_1()
    test_2()

    with pytest.raises(ValueError): dts.addEndsBefore("2000-12-31T23:59:59Z")
    with pytest.raises(ValueError): dts.addEndsBefore("2020-12-31T23:59:59Z")
    with pytest.raises(ValueError): dts.addEndsBefore("1900-12-31T23:59:59Z")
    test_1()
    test_2()
        
if __name__ == "__main__":
    t = DateTimeRange.ts2dt(1504512814466)
    print t
    u = DateTimeRange.dt2ts("2017-09-04T08:13:34.466000")
    print u
    print (u - 1504512814466) == 0
    print t == "2017-09-04T08:13:34.466000"
    
    print datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
    print DateTimeRange.ts2dt(0)
    print DateTimeRange.ts2dt(-10000)
#     print datetime.strptime("2017-09-04", "%Y-%m-%d")
#     print datetime.strptime("2017-09-04T12:00:00", "%Y-%m-%dT%H:%M:%S")
#     print datetime.strptime("2017-09-04T13", "%Y-%m-%dT%H:%M:%S")
    
    
    
      