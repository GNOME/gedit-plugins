#! /usr/bin/env python
import sys
import StringIO
block = sys.stdin.read()
block = StringIO.StringIO(block)
for line in block:
	if "-- " in line:
		line = line.translate(None, '-- ')
	else:
		line = "-- " + line
	sys.stdout.write(line)
exit()
## Set gedit external tools params as below:
## "Save" ==> "Current Document"
## "Input" ==> "Current Selection"
## "Output" ==> "Replace Current Selection"
