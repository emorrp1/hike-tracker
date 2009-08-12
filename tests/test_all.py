#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest
import test_base, test_route, test_team

class TestTracker(unittest.TestCase):
	def setUp(self):
		start('test')

	def tearDown(self):
		elixir.session.close()

	def testGet(self):
		self.assertEqual(get('b0'), model.Base.get_by(name='0'))
		self.assertEqual(get('r1'), model.Route.get_by(name='1'))
		self.assertEqual(get('t3'), model.Team.get_by(name='3'))

def suite():
	tracker_suite = unittest.TestLoader().loadTestsFromTestCase(TestTracker)
	base_suite = test_base.suite()
	route_suite = test_route.suite()
	team_suite = test_team.suite()
	return unittest.TestSuite([tracker_suite, base_suite, route_suite, team_suite])

if __name__ == '__main__':
	start('test')
	exec(open('test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import system
	system('rm test.hike')
