from elixir import *
from model import *

def start(filename="custom.hike"):
	from os.path import exists
	metadata.bind = "sqlite:///" + filename # connect
	setup_all()
	if not exists(filename):
		create_all()

save = session.commit
