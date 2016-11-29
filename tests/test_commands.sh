#!/bin/bash

# Tests of teh TranskribusPyClient command-line utilities
# JL Meunier - Nov 29th 2016
#
# Copyright Xerox(C) 2016 H. Déjean, JL. Meunier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Developed  for the EU project READ. The READ project has received funding 
# from the European Union?s Horizon 2020 research and innovation programme 
# under grant agreement No 674943.

# ------------------------------------------------------------------------------------------------------------------------
# ---  CONFIGURATION SECTION
# ------------------------------------------------------------------------------------------------------------------------

#transkribus valid login
login="jean-luc.meunier@xrce.xerox.com"
passwd="trnjluc"

#some existing collection with read access
coldId=3571
#2 documents, forming a small range
docId_A=7749
docId_B=7750


PYTHON=python
SRC=`dirname "$0"`/../src

#some valid sandbox collection
colId=3820

# ------------------------------------------------------------------------------------------------------------------------
# ---  GENERIC STUF BELOW
# ------------------------------------------------------------------------------------------------------------------------

tmp_col_name="toto_$$"

# ------------------------------------------------------------------------------------------------------------------------

function error {
	echo "ERROR: $1"
	exit 1
}

# ------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------
#cleaning
echo
echo "- logout"
tmp_col_id=`$PYTHON $SRC/TranskribusCommands/do_logout.py --persist`
echo "OK"

#bad login
echo
echo "- login"
tmp_col_id=`$PYTHON $SRC/TranskribusCommands/do_login.py --persist -l "tilla" -p "miaouuuu"` && error "login should have failed"
echo "OK"

echo
echo "- login"
tmp_col_id=`$PYTHON $SRC/TranskribusCommands/do_login.py --persist -l "$login" -p "$passwd"` || error "login error"
echo "OK"

#---------------------------------------------------

echo
echo "- creating a collection $tmp_col_name"
tmp_col_id=`$PYTHON $SRC/TranskribusCommands/do_createCollec.py --persist $tmp_col_name` || error "collection creation error"
echo "--> $tmp_col_id"

#---------------------------------------------------
echo
echo "- adding doc $docId_A - $docId_B to the new collection"
$PYTHON $SRC/TranskribusCommands/do_addDocToCollec.py --persist $tmp_col_id $docId_A  || error "collection add error 1"
echo "OK"

echo
echo "- adding doc $docId_A - $docId_B to the new collection"
$PYTHON $SRC/TranskribusCommands/do_addDocToCollec.py --persist $tmp_col_id $docId_A-$docId_B  || error "collection add error 2"
echo "OK"

echo
echo "- copying doc $docId_A from collection $colId to the new collection"
$PYTHON $SRC/TranskribusCommands/do_copyDocToCollec.py --persist $colId $tmp_col_id $docId_A  || error "collection copy error 1"
echo "OK"


#---------------------------------------------------

echo
echo "- listing collection $colId "
$PYTHON $SRC/TranskribusCommands/do_listCollec.py --persist $colId  || error "collection list error"
echo "OK"

#---------------------------------------------------
echo
echo "- deleting it ($tmp_col_id)"
tmp_col_id=`$PYTHON $SRC/TranskribusCommands/do_deleteCollec.py --persist $tmp_col_id` || error "collection deletion error"
echo "--> done"


