#
# A simple trace module
# 
# JL Meunier - May 2004
# Copyright XRCE, 2004
#

import sys

global traceFD
traceFD = sys.stderr

def setTraceFD(fd):
    global traceFD
    traceFD = fd
     
def trace(*msg):
    global traceFD
    for i in msg:
        try: traceFD.write(str(i))
        except UnicodeEncodeError:sys.stderr.write(i.encode("utf-8"))

def traceln(*msg):
    global traceFD
    
    apply(trace, msg)
    trace("\n")
    traceFD.flush()




#SELF-TEST
if __name__=="__main__":

    trace(1)
    trace(" aut")
    trace("o")
    traceln("-test")
    trace("2 auto", "-", "test")
    trace()
    traceln()
    traceln("Done")
