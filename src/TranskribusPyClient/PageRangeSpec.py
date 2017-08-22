# -*- coding: utf-8 -*-

"""
    Page range specification for Python clients
    
    A class to deal with page range specifications like 1-5,8
    
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

class PageRangeSpec:
    def __init__(self, sPageRange=""):
        self._ltAB = self.parseSpec(sPageRange)
        assert str(self) == "".join(sPageRange.split())
        
    @classmethod
    def parseSpec(cls, sSpec):
        """
        parse a page range spec and return a list of pair of page indices
        """
        ltAB = list()
        prev_b = None
        for sPageRange in sSpec.split(","):
            if not sPageRange.split(): continue #empty spec!
            lsN = sPageRange.split('-')
            if len(lsN) == 1:
                a = int(lsN[0])
                b = a
            elif len(lsN) == 2:
                a,b = int(lsN[0]), int(lsN[1])
            else:
                raise ValueError("invalid range: '%s'"%sPageRange)
            if not(a<=b): raise ValueError("Invalid range: '%s'"%sPageRange)
            ltAB.append( (a,b) )
            if prev_b < a:
                prev_b = b
            else:
                raise ValueError("unordered or overlapping ranges: '%d' >= '%d' '%s'"%(prev_b, a, sSpec))
        return ltAB
        
    def __str__(self): return ",".join( "%d-%d"%(a,b) if a != b else "%d"%a for (a,b) in self._ltAB )
    
    def __iter__(self):
        """
        Iterator returning each page number in turn
        """    
        for a,b in self._ltAB:
            for n in range(a,b+1):
                yield n
        raise StopIteration
    
    def __len__(self):
        return sum(b-a+1 for a,b in self._ltAB)
        
def test_good_spec():
    o = PageRangeSpec("1")
    assert list(o) == [1]
    
    o = PageRangeSpec("99")
    assert list(o) == [99]    
    
    o = PageRangeSpec("1,99")
    assert list(o) == [1, 99]      
    
    o = PageRangeSpec("1-5")
    assert list(o) == range(1, 6)

    o = PageRangeSpec("1-5,6-88")
    assert list(o) == range(1, 6)+range(6, 89)          
    
    o = PageRangeSpec("1-3,4-8")
    assert list(o) == range(1, 9)   
    assert len(o) == len(range(1, 9)) 

def test_spaced_good_spec():
    o = PageRangeSpec(" 1\t\t")
    assert list(o) == [1]
    
    o = PageRangeSpec("99  ")
    assert list(o) == [99]    
    
    o = PageRangeSpec("1  , 99")
    assert list(o) == [1, 99]      
    
    o = PageRangeSpec(" 1\t- 5\t")
    assert list(o) == range(1, 6)

    o = PageRangeSpec("1-5, 6-88")
    assert list(o) == range(1, 6)+range(6, 89)          
    
    o = PageRangeSpec("1 -3\t,4- 8")
    assert list(o) == range(1, 9)   
    assert len(o) == len(range(1, 9)) 

    
def test_errors():
    import pytest
    with pytest.raises(ValueError): PageRangeSpec("1 3")
    with pytest.raises(ValueError): PageRangeSpec("3-1")
    with pytest.raises(ValueError): PageRangeSpec("3,1")
    with pytest.raises(ValueError): PageRangeSpec("1-3,2")
    with pytest.raises(ValueError): PageRangeSpec("3,1-2")
    with pytest.raises(ValueError): PageRangeSpec("1-3,3-8")
    with pytest.raises(ValueError): PageRangeSpec("1-3 3,3-8")
    with pytest.raises(ValueError): PageRangeSpec("1-3,3-8 8")
    

def test_limit():
    o = PageRangeSpec("")
    assert list(o) == []
    assert len(o) == 0
    o = PageRangeSpec("\t  \t ")
    assert list(o) == []
    assert len(o) == 0    