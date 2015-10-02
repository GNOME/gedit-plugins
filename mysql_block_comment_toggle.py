#! /usr/bin/env python
from __future__ import print_function
import sys
import commands
line = sys.stdin.read()
if "/*" and "*/" in line:
	##exit("Block already commented")
	line = line.translate(None, '/*')
	line = line.translate(None, '*/')
else:
	## line = sys.stdin.read().replace("\r","")
	line = "/*" + line
	line = line + "*/"
# print line
sys.stdout.write(line)
## Set gedit external tools params as below:
## "Save" ==> "Current Document"
## "Input" ==> "Current Selection"
## "Output" ==> "Replace Current Selection"
