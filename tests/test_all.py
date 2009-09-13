#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest
import test_base, test_route, test_team

class TestTracker(unittest.TestCase):
	def setUp(self):
		start('tests/test')

	def tearDown(self):
		elixir.session.close()

	def testGet(self):
		self.assertEqual(get('b0'), model.Base.get('0'))
		self.assertEqual(get('r1'), model.Route.get('1'))
		self.assertEqual(get('t3'), model.Team.get('3'))

	def testSetDistances(self):
		from configobj import ConfigObj
		from convert import set_distances
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
		from convert import set_distances
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
		from convert import set_distances
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

	def testReportStoppage(self):
		from datetime import timedelta
		r = model.Report('0','1','15:34','16:17')
		self.assertEqual(r.stoppage(), timedelta(0,43*60))

	def testConvert(self):
		from os import system, remove
		tmpfile = 'tests/temp.conf'
		system('./convert.py tests/test.hike %s' % tmpfile)
		f = open('tests/test.conf')
		g = open(tmpfile)
		self.assertEqual(f.read(), g.read())
		f.close()
		g.close()
		remove(tmpfile)

	def testLoadAuto(self):
		from os import remove
		elixir.session.close()
		try:     start('tests/test_auto')
		except:  self.fail()
		finally: remove('tests/test_auto.hike')

	def testBaseReport(self):
		from datetime import timedelta
		b0 = get('b0')
		base_report(b0, 'tests/b0.report')
		b0.reports.sort(reverse=True)
		r = b0.reports
		self.assertEqual(r[0].stoppage(), timedelta(0,15*60))
		self.assertEqual(r[1].team, get('t4'))
		self.assertEqual(r[2].arr, model.mkdt('12:55'))
		self.assertEqual(r[3].base, b0)

def suite():
	tracker_suite = unittest.TestLoader().loadTestsFromTestCase(TestTracker)
	base_suite = test_base.suite()
	route_suite = test_route.suite()
	team_suite = test_team.suite()
	return unittest.TestSuite([tracker_suite, base_suite, route_suite, team_suite])

if __name__ == '__main__':
	start('tests/test')
	exec(open('tests/test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import system
	system('rm tests/test.hike')
