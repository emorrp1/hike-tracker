#!/usr/bin/python -W ignore::DeprecationWarning
import elixir
import model

def save(config=False):
	elixir.session.commit()
	if config:
		from configobj import ConfigObj
		from os.path import expanduser
		config = expanduser(config + '.conf')
		config = ConfigObj(config)
		config['start'] = model.Config.get_by(key='start').value
		config['wiggle'] = model.Config.get_by(key='wfact').value
		config['figs'] = model.Config.get_by(key='figs').value
		bs = model.Base.query.all()
		if bs:
			config['bases'] = {}
			if model.Distance.query.all():
				config['distances'] = {}
			for b in bs:
				config['bases'][b.name] = b.ref()
				ds = model.Distance.query.filter_by(start=b)
				if ds.count():
					config['distances'][b.name] = []
					for d in ds:
						item = '%s:%d' % (d.end.name, d.distance)
						config['distances'][b.name].append(item)
			rs = model.Route.query.all()
			if rs:
				config['routes'] = {}
				for r in rs:
					config['routes'][r.name] = []
					for b in r.bases:
						config['routes'][r.name].append(b.name)
		ts = model.Team.query.all()
		if ts:
			config['teams'] = {}
			for t in ts:
				time = t.start.strftime('%H:%M')
				config['teams'][t.name] = [t.route.name, time]
		config.write()

if __name__ == '__main__':
	from sys import argv
	elixir.metadata.bind = 'sqlite:///%s' % argv[1]
	elixir.setup_all()
	save(argv[2])
