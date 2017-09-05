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

from common.IntegerRangeHalfBounded import IntegerRangeHalfBounded


class DateTimeRangeSpec(IntegerRangeHalfBounded):
    """
    A list of datetime range object
    
    - date time have the form: 2017-09-04 --aft 2017-09-04T14:00         (before the 1st date and after the second one)

    - the object is a container that supports:
        - contains test (if n in o: ...)
    """
    dt0 = datetime.datetime(1970, 1, 1)
    ts0 = 0
    
    def __init__(self):
        IntegerRangeHalfBounded.__init__(self)

    def add(self, sDateTimeA_or_dt, sDateTimeB_or_dt):
        """
        add a range
        """
        tsA = self.dt2ts(sDateTimeA_or_dt)
        tsB = self.dt2ts(sDateTimeB_or_dt)
        self.addRange(tsA, tsB)
        
    def addStartsAfter(self, sDateTimeA_or_dt):
        """
        Start of the interval
        """
        tsA = self.dt2ts(sDateTimeA_or_dt)
        self.addRange(tsA, self.inf())
       
    def addEndsBefore(self, sDateTimeB_or_dt):
        """
        end of the interval
        """
        tsB = self.dt2ts(sDateTimeB_or_dt)
        self.addRange(-self.inf(), tsB)

    @classmethod
    def dt2ts(cls, dt_or_s):
        """
        get either a datetime object or a textual date that is parsed. (Must be in form: "%Y-%m-%dT%H:%M:%S.%f")
        
        return a timestamp  (number of milliseconds since Thu Jan 01 01:00:00 1970)
        """
        if type(dt_or_s) == types.StringType:
            dt = None
            for i in range(7, 0, -1):  #from "%Y-%m-%dT%H:%M:%S"  to "%Y"
                sFmt = "".join(["%Y", "-%m", "-%d", "T%H", ":%M", ":%S", ".%f"][0:i])
                try:
                    dt = datetime.datetime.strptime(dt_or_s, sFmt)
                    break
                except ValueError:
                    pass
        else:
            dt = dt_or_s
            
        if dt == None: raise ValueError("Invalid textual date or datetime object: %s"%dt_or_s)
        
        ts = int((dt-cls.dt0).total_seconds() * 1000)
        #assert cls.format(cls.ts2dt(ts)).startswith(sDateTime)

        return ts

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
                
        dt = datetime.datetime.utcfromtimestamp(ts/1000.0)
        return dt

    @classmethod
    def format(cls, o):
        """
        takes a timestamp or a datetime
        return a textual date time in ISO format
        """
        try:
            ts = long(o)
            dt = DateTimeRangeSpec.ts2dt(ts)
        except TypeError:
            dt = o
        return dt.isoformat()
            
        
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
        
    o = DateTimeRangeSpec("1")
#     with capsys.disabled():
#         print "YOOOOOOOOOOOOOOOOOOOOOOOOOOO ", list(reversed(o))    
    container_test(o, [1])
    
    import pytest
    with pytest.raises(ValueError): DateTimeRangeSpec("1 3")
"""

    
def test_class_methods():
    import pytest

    assert datetime.datetime(1970, 1, 1) == DateTimeRangeSpec.ts2dt(0)
    assert datetime.datetime(1970, 1, 1) == DateTimeRangeSpec.ts2dt("0")
    assert DateTimeRangeSpec.ts2dt(-10000)
    with pytest.raises(ValueError): DateTimeRangeSpec.ts2dt("yo man")
    
    assert DateTimeRangeSpec.dt2ts("1970-01-01T00:00:00") == 0
    assert DateTimeRangeSpec.dt2ts("1969-12-31T23:59:00") == -60000
    with pytest.raises(ValueError): DateTimeRangeSpec.ts2dt("yo man")
    
    assert DateTimeRangeSpec.format(0) == "1970-01-01T00:00:00"
    assert DateTimeRangeSpec.format(datetime.datetime(1970, 1, 1)) == "1970-01-01T00:00:00"
    
    ts = 1504615116779
    dt = datetime.datetime(2017, 9, 5, 12, 38, 36, 779000)
    assert DateTimeRangeSpec.ts2dt(1504615116779) == dt
    
def test_simple():
    import pytest
    dts = DateTimeRangeSpec()
    dts.add("2017-09-04T12:00:00", "2017-09-04T23:00:00")
    
    assert DateTimeRangeSpec.dt2ts("2017-09-04T12:00:00") in dts
    assert DateTimeRangeSpec.dt2ts("2017-09-04T18:30:20") in dts
    assert DateTimeRangeSpec.dt2ts("2017-09-04T23:00:00") in dts
    assert DateTimeRangeSpec.dt2ts("2019-09") not in dts
    assert DateTimeRangeSpec.dt2ts("2010") not in dts
    
    #with pytest.raises(ValueError): 
    dts.addStartsAfter("2018-01-01")
    def test_1():
        assert DateTimeRangeSpec.dt2ts("2019-09") in dts
        assert DateTimeRangeSpec.dt2ts("2010") not in dts
        assert DateTimeRangeSpec.dt2ts("2017-12-31T23:59:59") not in dts
    test_1()

    with pytest.raises(ValueError): dts.addStartsAfter("2018-01-01")
    with pytest.raises(ValueError): dts.addStartsAfter("2012-01-01")
    with pytest.raises(ValueError): dts.addStartsAfter("2022-01-01")
    test_1()

    dts.addEndsBefore("2000-12-31T23:59:59")
    def test_2():
        assert DateTimeRangeSpec.dt2ts("1990-10-29T19:00") in dts
        assert DateTimeRangeSpec.dt2ts("2000-12-31T23:59:59") in dts
        assert DateTimeRangeSpec.dt2ts("2000-12-31T23:59:58") in dts
        assert DateTimeRangeSpec.dt2ts("2001-01-01T00:00:00") not in dts
    test_1()
    test_2()

    with pytest.raises(ValueError): dts.addEndsBefore("2000-12-31T23:59:59")
    with pytest.raises(ValueError): dts.addEndsBefore("2020-12-31T23:59:59")
    with pytest.raises(ValueError): dts.addEndsBefore("1900-12-31T23:59:59")
    test_1()
    test_2()
        
if __name__ == "__main__":
    t = DateTimeRangeSpec.ts2dt(1504512814466)
    print t
    u = DateTimeRangeSpec.dt2ts("2017-09-04T08:13:34.466000")
    print u
    print (u - 1504512814466) == 0
    print t == "2017-09-04T08:13:34.466000"
    
    print datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
    print DateTimeRangeSpec.ts2dt(0)
    print DateTimeRangeSpec.ts2dt(-10000)
#     print datetime.strptime("2017-09-04", "%Y-%m-%d")
#     print datetime.strptime("2017-09-04T12:00:00", "%Y-%m-%dT%H:%M:%S")
#     print datetime.strptime("2017-09-04T13", "%Y-%m-%dT%H:%M:%S")
    
    
    
      