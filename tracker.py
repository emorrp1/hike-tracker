#!/usr/bin/env python3
from model import *

VERSION += '.0'
__version__ = VERSION

def start(hike='custom'):
	'''Start the database connection, creating the tables and configuring if necessary'''
	from os.path import exists, expanduser
	hike = expanduser(hike + '.hike')
	db.Entity.metadata.bind = 'sqlite:///%s' % hike
	if not exists(hike):
		from convert import load
		db.Entity.metadata.create_all()
		hike = hike.replace('.hike', '.conf')
		load(hike)

def save():
	db.session.commit()

def all(type):
	'''Shortcut to a list of specified hike objects'''
	types = {'b':Base, 'r':Route, 't':Team}
	t = type[0].lower()
	return types[t].query.all()

def get(tname):
	'''Shortcut to getting hike objects by name'''
	type = tname[0].lower()
	name = tname[1:]
	types = {'b':Base, 'r':Route, 't':Team}
	return types[type].get(name)

def get_all(type=None):
	'''Load all objects into global namespace'''
	types = {'b':Base, 'r':Route, 't':Team}
	if type:
		t = type[0].lower()
		for i in all(t):
			tname = t + i.name
			line = '%s = get("%s")' % (tname, tname)
			exec(line, globals())
	else:
		for t in types:
			get_all(t)

def base_report(base, filename=None):
	if filename:
		f = open(filename)
	else:
		from sys import stdin
		f = stdin
	for line in f.readlines():
		kwargs = {}
		args = [base]
		for arg in line.split():
			if '=' in arg:
				k,v = arg.split('=')
				kwargs[k] = v
			else:
				args += [arg]
		try:
			Report(*args, **kwargs)
		except Exception as e:
			print(args, kwargs, e)

if __name__ == '__main__':
	from os import environ as _environ
	_environ["PYTHONINSPECT"] = "1"
	from sys import argv
	if len(argv) >= 2:
		start(argv[1][:-5])
