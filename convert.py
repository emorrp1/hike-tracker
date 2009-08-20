
def start(hike='custom'):
	'''Start the database connection, creating the tables and configuring if necessary'''
	from os.path import exists, expanduser
	hike = expanduser(hike + '.hike')
	elixir.metadata.bind = 'sqlite:///%s' % hike
	elixir.setup_all()
	if exists(hike):
		model.Config.load()
	else:
		elixir.create_all()
		configure(hike[:-5])
		save()

def save(config=False):
	model.Config.store()
	elixir.session.commit()
	if config:
		from configobj import ConfigObj
		from os.path import expanduser
		config = expanduser(config + '.conf')
		config = ConfigObj(config)
		config['start'] = model.config['start'].strftime('%y%m%d%H:%M')
		config['wiggle'] = model.config['wfact']
		config['figs'] = model.config['figs']*2
		bs = all('bases')
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
			rs = all('routes')
			if rs:
				config['routes'] = {}
				for r in rs:
					config['routes'][r.name] = []
					for b in r.bases:
						config['routes'][r.name].append(b.name)
		ts = all('teams')
		if ts:
			config['teams'] = {}
			for t in ts:
				time = t.start.strftime('%H:%M')
				config['teams'][t.name] = [t.route.name, time]
		config.write()

