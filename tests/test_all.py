#!/usr/bin/env python3
from tracker import *
import unittest
import test_base, test_route, test_team

class TestTracker(unittest.TestCase):
	def setUp(self):
		start('tests/test')

	def tearDown(self):
		db.session.close()

	def testGet(self):
		self.assertEqual(get('b0'), Base.get('0'))
		self.assertEqual(get('r1'), Route.get('1'))
		self.assertEqual(get('t3'), Team.get('3'))

	def testReportStoppage(self):
		from datetime import timedelta
		r = Report('0','1','15:34','16:17')
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
		db.session.close()
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
		self.assertEqual(r[2].arr, mkdt('12:55'))
		self.assertEqual(r[3].base, b0)

	def testLegDist(self):
		b0 = get('b0')
		b1 = get('b1')
		b75 = Base('75', '072056')
		conf().wfact = 1
		self.assertEqual(Leg.get(b0,b1).dist, 10)
		self.assertEqual(Leg.get(b0,b1).dist, Leg.get(b1,b0).dist)
		self.assertEqual(Leg.get(b0,get('b3')).dist, 14)
		self.assertEqual(Leg.get(b0,b75).dist, 91)

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
	from os import remove
	remove('tests/test.hike')
