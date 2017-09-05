# -*- coding: utf-8 -*-

"""
    Integer range specification for Python clients, supporting half-bounded intervals
    
    A class to deal with integer range specifications like 1-5,8, or 1-5,8-
    
    Copyright Naver(C) 2017, JL. Meunier, September 2017

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
from IntegerRange import IntegerRange

class IntegerRangeHalfBounded(IntegerRange):
    """
    A integer range object
    
    - at creation, pass a range specification of the form: 1  or 1-3  or 1,3  or 1,5-7,8 
        or 1-, -3, -5, 7, 9-,
            IntegerRangeHalfBounded = RANGE [, RANGE]+
        where RANGE is one of
            RANGE = N
            RANGE = N-N
            RANGE = N-
            RANGE = -N
        Spaces are ignored, apart between digits.
    - the object is a container that supports:
        - iteration         (possibly infinite!!)
        - len()
        - reversed()
        - contains test (if n in o: ...)
    """

    _fINF = float('inf')
    
    @classmethod
    def inf(cls): return float('inf')
    
    @classmethod
    def _getAB(cls, sRange):
        lsN = sRange.split('-')
        if len(lsN) == 1:
            a = int(lsN[0])
            b = a
        elif len(lsN) == 2:
            sA, sB = lsN
            a = int(sA) if sA else -cls._fINF
            b = int(sB) if sB else +cls._fINF
            if not(a<=b): raise ValueError("Invalid range: '%s'"%sRange)
        else:
            raise ValueError("invalid range: '%s'"%sRange)        
        return a, b

    def __str__(self): 
        return ",".join( "%s-%s"%(a,b) if a != b else "%s"%a for (a,b) in [( a if a!=-self._fINF else ""
                                                                          , b if b!=+self._fINF else "") for a,b in self._ltAB] )

    #--- Emulating Container type...
    def __iter__(self):
        """
        Iterator returning each number in turn
        """    
        for a,b in self._ltAB:
            if a == -self._fINF: raise ValueError("Cannot iterate starting from -infinite")
            i = a
            while i <= b:
                yield i
                i += 1
        raise StopIteration
    
    def __reversed__(self):
        """
        Reversed iterator
        If we do not provide it, we must provide a __getitem__ (boring to code and how useful??)
        """
        for a,b in reversed(self._ltAB):
            if b == self._fINF: raise ValueError("Cannot iterate starting from +infinite")
            i = b
            while a <= i:
                yield i
                i -= 1        
        raise StopIteration        

    def __len__(self):
        #__len__() should return an int 
        v = IntegerRange.__len__(self)
        if v == self._fINF:
            raise ValueError("Infinite length. Builtin 'len' cannot be used, consider the method 'len' of this object.")
        else:
            return v
    
# ------ TESTS ----------------------------------------------------------------------------------
def test_good_spec(capsys):
    def container_test(o, lref):
        assert list(o) == lref
        assert list(reversed(o)) == list(reversed(lref))
        for item in lref: assert item in o
        assert -99 not in o
        
    o = IntegerRangeHalfBounded("1")
    if False:
        with capsys.disabled():
            print "YOOOOOOOOOOOOOOOOOOOOOOOOOOO ", list(reversed(o))    
    container_test(o, [1])
    
    o = IntegerRangeHalfBounded("99")
    container_test(o, [99])    
    
    o = IntegerRangeHalfBounded("1,99")
    container_test(o, [1, 99])      
    
    o = IntegerRangeHalfBounded("1-5")
    container_test(o, range(1, 6))

    o = IntegerRangeHalfBounded("1-5,6-88")
    container_test(o, range(1, 6)+range(6, 89))          
    
    o = IntegerRangeHalfBounded("1-3,4-8")
    container_test(o, range(1, 9))   
    assert len(o) == len(range(1, 9)) 
    

def test_spaced_good_spec():
    def container_test(o, lref):
        assert list(o) == lref
        assert list(reversed(o))== list(reversed(lref))
        for item in lref: assert item in o
        assert -99 not in o
        
    o = IntegerRangeHalfBounded(" 1\t\t")
    container_test(o, [1])
    
    o = IntegerRangeHalfBounded("99  ")
    container_test(o, [99])    
    
    o = IntegerRangeHalfBounded("1  , 99")
    container_test(o, [1, 99])      
    
    o = IntegerRangeHalfBounded(" 1\t- 5\t")
    container_test(o, range(1, 6))

    o = IntegerRangeHalfBounded("1-5, 6-88")
    container_test(o, range(1, 6)+range(6, 89))          
    
    o = IntegerRangeHalfBounded("1 -3\t,4- 8")
    container_test(o, range(1, 9))
    assert len(o) == len(range(1, 9)) 

def test_errors():
    import pytest
    with pytest.raises(ValueError): IntegerRangeHalfBounded("1 3")
    with pytest.raises(ValueError): IntegerRangeHalfBounded("3-1")
    with pytest.raises(ValueError): IntegerRangeHalfBounded("3,1")
    with pytest.raises(ValueError): IntegerRangeHalfBounded("1-3,2")
    with pytest.raises(ValueError): IntegerRangeHalfBounded("3,1-2")
    with pytest.raises(ValueError): IntegerRangeHalfBounded("1-3,3-8")
    with pytest.raises(ValueError): IntegerRangeHalfBounded("1-3 3,3-8")
    with pytest.raises(ValueError): IntegerRangeHalfBounded("1-3,3-8 8")
    

def test_limit():
    o = IntegerRangeHalfBounded("")
    assert list(o) == []
    assert len(o) == 0
    o = IntegerRangeHalfBounded("\t  \t ")
    assert list(o) == []
    assert len(o) == 0  

def test_add():
    import pytest

    def container_test(o, lref):
        assert list(o) == lref
        assert list(reversed(o)) == list(reversed(lref))
        for item in lref: assert item in o
        assert -99 not in o
        
    o = IntegerRange()
    container_test(o, [])
    
    o.addRange(1)
    container_test(o, [1])

    o.addRange(0)
    container_test(o, [0, 1])    
    
    with pytest.raises(ValueError): o.addRange(1)
    with pytest.raises(ValueError): o.addRange(0,1)
    with pytest.raises(ValueError): o.addRange(-3,0)
    with pytest.raises(ValueError): o.addRange(-3,3)
    with pytest.raises(ValueError): o.addRange(1,3)
    with pytest.raises(ValueError): o.addRange(0,3)
    
    o.addRange(90, 99)
    container_test(o, [0, 1]+range(90, 100))    
    
    o.addRange(60, 66)
    container_test(o, [0, 1]+range(60, 67)+range(90, 100))    
    
    with pytest.raises(ValueError): o.addRange(0,1000)
    with pytest.raises(ValueError): o.addRange(10,60)
    with pytest.raises(ValueError): o.addRange(70,95)
    with pytest.raises(ValueError): o.addRange(95)
    o.addRange(80, 88)
    container_test(o, [0, 1]+range(60, 67)+range(80, 89)+range(90, 100))    
    
        
    
#half-bounded tests
def test_good_spec_halfbounded(capsys):
    import pytest
    o = IntegerRangeHalfBounded("1-")
    itr = iter(o)
    assert [itr.next() for i in range(10)] == range(1, 11)
    assert -99 not in o

    o = IntegerRangeHalfBounded("1-5,6-")
    itr = iter(o)
    assert [itr.next() for i in range(1, 11)] == range(1, 11)
    for i in range(1, 100): assert i in o
    assert o.len() == float('inf') 
    itr = reversed(o)
    with pytest.raises(ValueError): itr.next() 
    
    o = IntegerRangeHalfBounded("-8")
    itr = reversed(o)
    assert [itr.next() for i in range(10)] == range(8, -2, -1)
    
    with pytest.raises(ValueError):  len(o) 
    itr = iter(o)
    with pytest.raises(ValueError): itr.next() 


    o = IntegerRangeHalfBounded("-5,7-")
    itr = iter(o)
    with pytest.raises(ValueError): itr.next() 
    itr = reversed(o)
    with pytest.raises(ValueError): itr.next() 
    assert -5555 in o
    assert 5 in o
    assert 7 in o
    assert 7777 in o
    assert 6 not in o
    

def test_add_halfbounded():
    import pytest

    def container_test(o, lref):
        assert list(o) == lref
        assert list(reversed(o)) == list(reversed(lref))
        for item in lref: assert item in o
        assert -99 not in o
        
    o = IntegerRangeHalfBounded()
    container_test(o, [])
    
    
    o.addRange(100)
    assert list(o) == [100]

    inf = float('inf')
    o.addRange(-inf, 0)
    
    with pytest.raises(ValueError): o.addRange(0)
    with pytest.raises(ValueError): o.addRange(-100, -3)
    with pytest.raises(ValueError): o.addRange(0, inf)
    with pytest.raises(ValueError): o.addRange(-3,3)
    with pytest.raises(ValueError): o.addRange(0,3)
    with pytest.raises(ValueError): o.addRange(-3,3)

    itr = reversed(o)
    assert [itr.next(), itr.next(), itr.next(), itr.next()] == [100, 0, -1, -2]
    
    o.addRange(1000, inf)
    with pytest.raises(ValueError): o.addRange(2000)

    with pytest.raises(ValueError): o.addRange(0)
    with pytest.raises(ValueError): o.addRange(-100, -3)
    with pytest.raises(ValueError): o.addRange(0, inf)
    with pytest.raises(ValueError): o.addRange(-3,3)
    with pytest.raises(ValueError): o.addRange(0,3)
    with pytest.raises(ValueError): o.addRange(-3,3)
    
    assert -100 in o    
    assert -10  in o    
    assert -1   in o    
    assert  0   in o    
    assert  1   not in o    
    assert 10   not in o    
    assert 100  in o    
    assert 200  not in o    
    assert 999  not in o    
    assert 1000 in o    
    assert 2000 in o    
    assert 9999 in o    
    
#     o.addRange(90, 99)
#     container_test(o, [0, 1]+range(90, 100))    
#     
#     o.addRange(60, 66)
#     container_test(o, [0, 1]+range(60, 67)+range(90, 100))    
#     
#     with pytest.raises(ValueError): o.addRange(0,1000)
#     with pytest.raises(ValueError): o.addRange(10,60)
#     with pytest.raises(ValueError): o.addRange(70,95)
#     with pytest.raises(ValueError): o.addRange(95)
#     o.addRange(80, 88)
#     container_test(o, [0, 1]+range(60, 67)+range(80, 89)+range(90, 100))    
    
        