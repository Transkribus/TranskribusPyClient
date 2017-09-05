# -*- coding: utf-8 -*-

"""
    Page range specification for Python clients
    
    A class to deal with page range specifications like 1-5,8
    
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

from common.IntegerRange import IntegerRange

class PageRangeSpec(IntegerRange):
    """
    A page range object
    
    - at creation, pass a page range specification of the form: 1  or 1-3  or 1,3  or 1,5-7,8
            PAGERANGESPEC = RANGE [, RANGE]+
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
    def __init__(self):
        IntegerRange.__init__(self)
