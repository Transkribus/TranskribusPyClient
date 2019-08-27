#!/bin/bash

# Tests of the TranskribusPyClient command-line utilities
#
# JL Meunier - Nov 29th 2016
#
# Copyright Xerox(C) 2016 H. Déjean, JL. Meunier
#
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
# from the European Union's Horizon 2020 research and innovation programme 
# under grant agreement No 674943.

# ------------------------------------------------------------------------------------------------------------------------
# ---  CONFIGURATION SECTION
# ------------------------------------------------------------------------------------------------------------------------

#transkribus valid login
login="herve.dejean@naverlabs.com"
passwd=""

#some existing collection with read access for you
colId=3571
#2 existing documents, forming a small range
docId_A=7749
docId_B=7750
TRP=tst.trp

#PYTHON=python
PYTHON=/drives/c/Local/anaconda3/envs/py36/python.exe

# ------------------------------------------------------------------------------------------------------------------------
# ---  GENERIC STUF BELOW
# ------------------------------------------------------------------------------------------------------------------------

SRC=`dirname "$0"`/../src

tmp_col_name="toto_$$"

# ------------------------------------------------------------------------------------------------------------------------

function error {
	echo "ERROR: $1"
	exit 1
}

# ------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------
#cleaning any persistent login info
echo "==================================================================="
echo "--- logout"
tmp_col_id=`$PYTHON $SRC/TranskribusCommands/do_logout.py --persist`
echo "OK"

#testing a bad login
echo
echo "--- login"
tmp_col_id=`$PYTHON $SRC/TranskribusCommands/do_login.py --persist -l "tilla" -p "miaouuuu"` && error "login should have failed"
echo
echo "OK"

#making a login and persisting the session token
echo
echo "--- login"
tmp_col_id=`$PYTHON $SRC/TranskribusCommands/do_login.py --persist -l "$login" -p "$passwd"` || error "login error"
echo "OK"

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="

echo
echo "--- creating a collection $tmp_col_name"
tmp_col_id=`$PYTHON $SRC/TranskribusCommands/do_createCollec.py --persist $tmp_col_name` || error "collection creation error"
echo "--> $tmp_col_id"
echo "OK"

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- adding doc $docId_A - $docId_B to the new collection"
$PYTHON $SRC/TranskribusCommands/do_addDocToCollec.py --persist $tmp_col_id $docId_A  || error "collection add error 1"
echo "OK"

echo
echo "--- adding doc $docId_A - $docId_B to the new collection"
$PYTHON $SRC/TranskribusCommands/do_addDocToCollec.py --persist $tmp_col_id $docId_A-$docId_B  || error "collection add error 2"
echo "OK"

echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- copying doc $docId_A from collection $colId to the new collection"
$PYTHON $SRC/TranskribusCommands/do_duplicateDoc.py --persist $colId $tmp_col_id $docId_A  || error "collection copy error 1"
echo "OK"

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- deleting it ( $tmp_col_id ) "
tmp_col_id=`$PYTHON $SRC/TranskribusCommands/do_deleteCollec.py --persist $tmp_col_id` || error "collection deletion error"
echo "OK"

echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- display  trpdoc of the first page of $docId_A from collection $colId "
$PYTHON $SRC/TranskribusCommands/do_getDocTrp.py --persist $colId $docId_A 1 || error "getDocTrp error 1"
echo "OK"



#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- listing collection $colId "
$PYTHON $SRC/TranskribusCommands/do_listCollec.py --persist $colId  || error "collection list error"
echo "OK"

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- Layout Analysis in collection $colId "
$PYTHON $SRC/TranskribusCommands/do_analyzeLayout.py $colId $docId_A/1  || error "layout analysis error"
echo "OK"

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- delete last transcript $colid / $docid / 1 "
$PYTHON $SRC/TranskribusCommands/do_transcript.py $colId  $docId_A 1 --last --rm || error " delete last transcript error"
echo "OK"

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- list of locked pages for  $docId_A in  $colId "
$PYTHON $SRC/TranskribusCommands/do_listPageLocks.py $colId $docId_A   || error "locked pages error"
echo "OK"

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- list HTR models in collection $colId "
$PYTHON $SRC/TranskribusCommands/do_listHtrRnn.py --colid=$colId   || error "list HTR models error"
echo "OK"

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- list trpdoc for document  $docId_A in  $colId "
$PYTHON $SRC/TranskribusCommands/do_transcript.py $colId  $docId_A || error " transcript list models error"
echo "OK"


#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- save trpdoc for document  $docId_A in $TRP "
$PYTHON $SRC/TranskribusCommands/do_transcript.py $colId  $docId_A 2 --trp=$TRP || error " transcript list models error"

echo "OK"


#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- download as per trp ---"
rm -rf trnskrbs_$colId 
echo "--- download using $TRP "
$PYTHON $SRC/TranskribusCommands/Transkribus_downloader.py $colId  --trp=$TRP || error " download error"
echo "OK"
#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- download trnskrbs_$colId document $docId_A ---"
rm -rf trnskrbs_$colId 
echo "--- download document  $docId_A ($colId) "
$PYTHON $SRC/TranskribusCommands/Transkribus_downloader.py $colId  --docid=$docId_A --noimage || error " download error"
echo "OK"

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- upload  document  $docId_A ($colId ) "
$PYTHON $SRC/TranskribusCommands/TranskribusDU_transcriptUploader.py trnskrbs_$colId  $colId  $docId_A --nodu || error "  TranskribusDU_transcriptUploaderupload error"
echo "OK"

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- upload as per trp $TRP "
$PYTHON $SRC/TranskribusCommands/Transkribus_uploader.py trnskrbs_$colId  $colId  $docId_A --trp=$TRP || error " Transkribus_uploader upload error"
echo "OK"
echo "--- rm $TRP"
rm $TRP

#---------------------------------------------------
echo "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
echo
echo "--- test only --help"
$PYTHON $SRC/TranskribusCommands/do_htrTrainRnn.py --help

echo "==================================================================="
echo "TESTs done"




