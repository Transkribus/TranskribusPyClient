# -*- coding: utf-8 -*-
"""
    mpxml to pxml convertor
    
    @author: H Déjean
    
    READ project
    31/05/2017
""" 
from __future__ import absolute_import
from __future__ import  print_function
from __future__ import unicode_literals
import sys, os.path, optparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))))

from lxml import etree
import xml_formats.PageXml as PageXml
    
if __name__ == "__main__":
    
    usage = """
%s dir docid
Utility to create a set of pageXml XML files from a mpxml file.
""" % sys.argv[0]

    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option("--format", dest='bIndent',  action="store_true" , help="reformat/reindent the input")    
    parser.add_option("--dir", dest='destdir',  action="store", default='pxml' , help="directory ouptut")  
    (options, args) = parser.parse_args()

    try:
        dir  = args[0]
        docid= args[1]
    except:
        parser.print_help()
        parser.exit(1, "")
    
    sDocFilename = "%s%scol%s%s.mpxml" % (dir,os.sep,os.sep,docid)        
        
    doc = etree.parse(sDocFilename)

    for pnum, pageDoc in PageXml.MultiPageXml._iter_splitMultiPageXml(doc, bInPlace=False):
        outfilename = "%s%s%s%s%s_%03d.pxml" % (dir,os.sep,options.destdir,os.sep,docid,pnum)
        print(outfilename)        
        pageDoc.write(outfilename, xml_declaration ='UTF-8',encoding="utf-8", pretty_print = bool(options.bIndent))
    print ("DONE")    