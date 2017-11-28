# -*- coding: utf-8 -*-

"""
    Integer range specification for Python clients
    
    A class to deal with integer range specifications like 1-5,8
    
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

class IntegerRange:
    """
    A integer range object
    
    - at creation, pass a range specification of the form: 1  or 1-3  or 1,3  or 1,5-7,8
            IntegerRange = RANGE [, RANGE]+
        where RANGE if either an integer or 2 integer separated by a '-'
            RANGE = N
            RANGE = N-N
        Spaces are ignored, apart between digits.
    - the object is a container that supports:
        - iteration
        - len()
        - reversed()
        - contains test (if n in o: ...)
    """
    def __init__(self, sRange=""):
        self._ltAB = self.parseSpec(sRange)
        assert str(self) == "".join(sRange.split())

    def initFromEnumeration(self, lN):
        """
        create the list of ranges that exactly cover the enumeration. 
        """        
        if not lN: 
            pass
        elif len(lN) == 1:
            self.addRange(lN[0])
        else:
            lN = sorted(lN)
            A = lN[0]
            Nprev = A
            for N in lN[1:]:
                if Nprev+1 < N:
                    #hole in sequence, create an interval!
                    self.addRange(A, Nprev)
                    A = N
                Nprev = N
            self.addRange(A, Nprev)
        return self
    
    @classmethod
    def parseSpec(cls, sSpec):
        """
        parse a range specification of positive integers and return a list of pair of indices
        """
        ltAB = list()
        prev_b = None
        for sRange in sSpec.split(","):
            if not sRange.split(): continue #empty spec!
            a,b = cls._getAB(sRange)
            ltAB.append( (a,b) )
            if prev_b < a:
                prev_b = b
            else:
                raise ValueError("unordered or overlapping ranges: '%s' >= '%s' '%s'"%(prev_b, a, sSpec))
        return ltAB

    def addRange(self, a, b=None):
        if b==None: b = a
        assert a <= b
        self._ltAB.append( (a,b) )
        self._ltAB.sort()
        if not self._check():
            self._ltAB.remove( (a,b) )
            raise ValueError("Overlapping range")
        
    def len(self):
        """
        For som subclass, this method can be useful as it is not forced by Python to return an int (like for return float('inf'))
        """
        return sum(b-a+1 for a,b in self._ltAB)
    
    @classmethod
    def _getAB(cls, sRange):
        lsN = sRange.split('-')
        if len(lsN) == 1:
            a = int(lsN[0])
            b = a
        elif len(lsN) == 2:
            sA, sB = lsN
            a,b = int(sA), int(sB)
            if not(a<=b): raise ValueError("Invalid range: '%s'"%sRange)
        else:
            raise ValueError("invalid range: '%s'"%sRange)        
        return a, b
    
    def _check(self):
        """
        checking things are in order
        """
        prevB = None
        for a,b in self._ltAB:
            if prevB >= a: return False
            prevB = b
        return True
    
    def __str__(self): 
        return ",".join( "%s-%s"%(a,b) if a != b else "%s"%a for (a,b) in self._ltAB )

    def __bool__(self):
        return bool(self._ltAB)
    
    def __nonzero__(self):
        return bool(self._ltAB)

    #--- Emulating Container type...
    def __iter__(self):
        """
        Iterator returning each number in turn
        """    
        for a,b in self._ltAB:
            for n in range(a,b+1): yield n
        raise StopIteration
    
    def __reversed__(self):
        """
        Reversed iterator
        If we do not provide it, we must provide a __getitem__ (boring to code and how useful??)
        """
        for a,b in reversed(self._ltAB):
            for n in range(b,a-1,-1): yield n
        raise StopIteration        
        
    def __len__(self):
        return sum(b-a+1 for a,b in self._ltAB)

    def __contains__(self, item):
        try:
            item = long(item)
        except TypeError:
            raise ValueError("A range contains numeric values not %s"%type(item))
        #if type(item) != types.IntType and type(item) != types.LongType: raise ValueError("A range contains integer values not %s"%type(item))
        a, b = None, None
        for a,b in self._ltAB:
            if b >= item: break
            #print a, item, b
        return a<= item and item <= b



# ------ TESTS ----------------------------------------------------------------------------------
def test_good_spec(capsys):
    def container_test(o, lref):
        assert list(o) == lref
        assert list(reversed(o)) == list(reversed(lref))
        for item in lref: assert item in o
        assert -99 not in o
        
    o = IntegerRange("1")
#     with capsys.disabled():
#         print "YOOOOOOOOOOOOOOOOOOOOOOOOOOO ", list(reversed(o))    
    container_test(o, [1])
    
    o = IntegerRange("99")
    container_test(o, [99])    
    
    o = IntegerRange("1,99")
    container_test(o, [1, 99])      
    
    o = IntegerRange("1-5")
    container_test(o, range(1, 6))

    o = IntegerRange("1-5,6-88")
    container_test(o, range(1, 6)+range(6, 89))          
    
    o = IntegerRange("1-3,4-8")
    container_test(o, range(1, 9))   
    assert len(o) == len(range(1, 9)) 

def test_spaced_good_spec():
    def container_test(o, lref):
        assert list(o) == lref
        assert list(reversed(o))== list(reversed(lref))
        for item in lref: assert item in o
        assert -99 not in o
        
    o = IntegerRange(" 1\t\t")
    container_test(o, [1])
    
    o = IntegerRange("99  ")
    container_test(o, [99])    
    
    o = IntegerRange("1  , 99")
    container_test(o, [1, 99])      
    
    o = IntegerRange(" 1\t- 5\t")
    container_test(o, range(1, 6))

    o = IntegerRange("1-5, 6-88")
    container_test(o, range(1, 6)+range(6, 89))          
    
    o = IntegerRange("1 -3\t,4- 8")
    container_test(o, range(1, 9))
    assert len(o) == len(range(1, 9)) 

def test_errors():
    import pytest
    with pytest.raises(ValueError): IntegerRange("1 3")
    with pytest.raises(ValueError): IntegerRange("3-1")
    with pytest.raises(ValueError): IntegerRange("3,1")
    with pytest.raises(ValueError): IntegerRange("1-3,2")
    with pytest.raises(ValueError): IntegerRange("3,1-2")
    with pytest.raises(ValueError): IntegerRange("1-3,3-8")
    with pytest.raises(ValueError): IntegerRange("1-3 3,3-8")
    with pytest.raises(ValueError): IntegerRange("1-3,3-8 8")
    

def test_limit():
    o = IntegerRange("")
    assert list(o) == []
    assert len(o) == 0
    o = IntegerRange("\t  \t ")
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
    
    assert 1 in o
    assert 0 in o
    assert 90 in o
    assert 80 in o
    assert 60 in o
    assert 66 in o
    assert 99 in o
    assert 88 in o
    
    assert 50 not in o
    
def test_enum():
    def test_enum(l):
        ll = set(l)    
        o = IntegerRange()
        o.initFromEnumeration(l)
        assert set(o) == ll
    
    test_enum([])
    test_enum([2])
    test_enum([-2])
    test_enum([2,1])
    test_enum([1,2])
    test_enum([1,2,2]) #bad case that we cover anyway
    test_enum([1,2,4,2,5])
    test_enum([7,4,6,1])
    test_enum([0])
    
    
    