#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest
import test_base, test_route, test_team

class TestTracker(unittest.TestCase):
	def setUp(self):
		start('test')
		self.orig_dists = model.Base.distances.copy()

	def tearDown(self):
		elixir.session.close()
		model.Base.distances = self.orig_dists

	def testGet(self):
		self.assertEqual(get('b0'), model.Base.get_by(name='0'))
		self.assertEqual(get('r1'), model.Route.get_by(name='1'))
		self.assertEqual(get('t3'), model.Team.get_by(name='3'))

	def testSetDistances(self):
		from configobj import ConfigObj
		c = ConfigObj({'0':['1:56','2:37'], '1':['3:45']})
		set_distances(c)
		b0 = get('b0')
		b1 = get('b1')
		b2 = get('b2')
		b3 = get('b3')
		self.assertEqual(b0.distance(b0), 0)
		self.assertEqual(b0.distance(b1), 56)
		self.assertEqual(b0.distance(b2), 37)
		self.assertEqual(b3.distance(b1), 45)

	def testSetDistancesOverwrite(self):
		from configobj import ConfigObj
		c = ConfigObj({'0':['1:56','2:37','1:23'], '2':['0:45']})
		set_distances(c)
		b0 = get('b0')
		b1 = get('b1')
		b2 = get('b2')
		self.assertEqual(b0.distance(b1), 23)
		self.assertEqual(b0.distance(b2), b2.distance(b0))
		self.assertEqual(b0.distance(b2), 45)

	def testSetDistancesByRoute(self):
		from configobj import ConfigObj
		c = ConfigObj({'0':['3:27', '1:45'],'routes':{'2':['23'], '1':['32','54','14']}})
		set_distances(c)
		b0 = get('b0')
		b1 = get('b1')
		b2 = get('b2')
		b3 = get('b3')
		self.assertEqual(b0.distance(b2), 23)
		self.assertEqual(b0.distance(b1), 45)
		self.assertEqual(b1.distance(b3), 54)
		self.assertEqual(b3.distance(b2), 14)

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
