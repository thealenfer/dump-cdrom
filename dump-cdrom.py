#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands, sys

def run(cmd):
	print cmd
	err, raw = commands.getstatusoutput(cmd)
	if err != 0:
		sys.exit(raw)
	return raw

GREEN = "\033[01;32m"
RED   = "\033[01;31m"

for line in run('isoinfo -d -i /dev/cdrom').split('\n'):
	if line.startswith('Volume id:'):
		isoname = line.split(':')[1].strip()
		isoname = isoname.replace(' ','-')
		isoname = isoname.replace('64-bit','amd64') + '.iso'
		print RED,

	if line.startswith('Logical block size is:'):
		blocksize = int(line.split(':')[1].strip())
		print RED,

	if line.startswith('Volume size is:'):
		count = int(line.split(':')[1].strip()) / blocksize
		print RED,

	print '\n', line, GREEN,

print RED, '\n'
print 'count =', count, '[volsize / blocksize]', GREEN, '\n'


cmd  = 'dd status=none if=/dev/cdrom bs=%d count=%d | tee %s | md5sum ' % (blocksize,count,isoname)
cmd += '&& cat %s | md5sum' % (isoname,)
print run(cmd)