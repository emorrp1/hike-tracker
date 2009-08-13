#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest

class TestBase(unittest.TestCase):
	def setUp(self):
		start('test')

	def tearDown(self):
		elixir.session.close()

	def testDone(self):
		self.assertTrue(get('b0').done())
		self.assertFalse(get('b1').done())
		self.assertTrue(get('b2').done())
		self.assertFalse(get('b3').done())

	def testNext1(self):
		self.assertEqual(get('b0').next('1'), get('b1'))
		self.assertEqual(get('b1').next('1'), get('b3'))
		self.assertEqual(get('b3').next('1'), get('b2'))
		self.assertEqual(get('b2').next('1'), None)

	def testNext2(self):
		self.assertEqual(get('b0').next('2'), get('b2'))
		self.assertEqual(get('b2').next('2'), get('b3'))
		self.assertFalse(get('b3').next('2'))

	def testDist(self):
		b0 = get('b0')
		b1 = get('b1')
		b75 = model.Base('75', '072056')
		model.Base.wfact = 1
		self.assertEqual(b0.distance(b1), 10)
		self.assertEqual(b0.distance(b1), b1.distance(b0))
		self.assertEqual(b0.distance(get('b3')), 14)
		self.assertEqual(b0.distance(b75), 91)

	def testDistAlong(self):
		b0 = get('b0')
		b1 = get('b1')
		b3 = get('b3')
		d01 = b0.distance(b1)
		d13 = b1.distance(b3)
		along = b0.distance_along('1',b3)
		self.assertEqual(d01+d13, along)

	def testWiggleFactor(self):
		wf1 = 1.5
		wf2 = 3.0
		model.Base.wfact = wf1
		d1 = get('b0').distance(get('b1'))
		model.Base.wfact = wf2
		d2 = get('b0').distance(get('b1'))
		self.assertEqual(float(d2)/d1, wf2/wf1)

	def testReport(self):
		from datetime import datetime, timedelta
		b0 = get('b0')
		b0.report('b0.report')
		b0.reports.sort(reverse=True)
		r = b0.reports
		self.assertEqual(r[0].stoppage(), timedelta(0,30*60))
		self.assertEqual(r[1].team, get('t4'))
		self.assertEqual(r[2].arr, model.mkdt('12:55'))
		self.assertEqual(r[3].base, b0)

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestBase)

if __name__ == '__main__':
	start('test')
	exec(open('test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import system
	system('rm test.hike')
