#!/usr/bin/python -iW ignore::DeprecationWarning
import elixir
import model

def start(hike='custom'):
	'''Start the database connection, creating the tables and configuring if necessary'''
	from os.path import exists, expanduser
	hike = expanduser(hike + '.hike')
	elixir.metadata.bind = 'sqlite:///%s' % hike
	elixir.setup_all()
	if not exists(hike):
		from convert import load
		elixir.create_all()
		hike = hike.replace('.hike', '.conf')
		load(hike)

def save():
	elixir.session.commit()

def all(type):
	'''Shortcut to a list of specified hike objects'''
	types = {'b':model.Base, 'r':model.Route, 't':model.Team}
	t = type[0].lower()
	return types[t].query.all()

def get(tname):
	'''Shortcut to getting hike objects by name'''
	type = tname[0].lower()
	name = tname[1:]
	types = {'b':model.Base, 'r':model.Route, 't':model.Team}
	return types[type].get(name)

def get_all(type=None):
	'''Load all objects into global namespace'''
	types = {'b':model.Base, 'r':model.Route, 't':model.Team}
	if type:
		t = type[0].lower()
		for i in all(t):
			tname = t + i.name
			line = '%s = get("%s")' % (tname, tname)
			exec line in globals()
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
		model.Report(*args, **kwargs)

if __name__ == '__main__':
	from sys import argv
	if len(argv) >= 2:
		start(argv[1][:-5])
