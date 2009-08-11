#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import start
import unittest
import test_base, test_route, test_team

def suite():
	base_suite = test_base.suite()
	route_suite = test_route.suite()
	team_suite = test_team.suite()
	return unittest.TestSuite([base_suite, route_suite, team_suite])

if __name__ == '__main__':
	start('test')
	exec(open('test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import system
	system('rm test.hike')
