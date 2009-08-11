#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest

class Testing(unittest.TestCase):
	def setUp(self):
		start('test')

	def tearDown(self):
		elixir.session.close()

	def testBaseDone(self):
		self.assertTrue(get('b0').done())
		self.assertFalse(get('b1').done())
		self.assertTrue(get('b2').done())
		self.assertFalse(get('b3').done())

	def testBaseNext1(self):
		self.assertEqual(get('b0').next('1'), get('b1'))
		self.assertEqual(get('b1').next('1'), get('b3'))
		self.assertEqual(get('b3').next('1'), get('b2'))
		self.assertEqual(get('b2').next('1'), None)

	def testBaseNext2(self):
		self.assertEqual(get('b0').next('2'), get('b2'))
		self.assertEqual(get('b2').next('2'), get('b3'))
		self.assertEqual(get('b3').next('2'), None)

	def testBaseDist(self):
		b0 = get('b0')
		b1 = get('b1')
		b75 = model.Base('75', '072056')
		self.assertEqual(b0.distance(b1), 10)
		self.assertEqual(b1.distance(b0), 10)
		self.assertEqual(b0.distance(get('b3')), 14)
		self.assertEqual(b0.distance(b75), 91)

	def testBaseDistAlong(self):
		b0 = get('b0')
		b1 = get('b1')
		b3 = get('b3')
		d01 = b0.distance(b1)
		d13 = b1.distance(b3)
		along = b0.distance_along('1',b3)
		self.assertEqual(d01+d13, along)

	def testRouteEnd(self):
		b = model.Base('testend', '000000')
		r = get('r1')
		r.bases.append(b)
		self.assertEqual(b, r.end())

	def testRouteLen(self):
		r = get('r1')
		length = r.bases[0].distance_along(r, r.end())
		self.assertEqual(length, len(r))

	def testTeamCompleted(self):
		self.assertFalse(get('t1').completed())
		self.assertTrue(get('t2').completed())
		self.assertTrue(get('t3').completed())
		self.assertFalse(get('t4').completed())

	def testTeam1Finishing(self):
		self.assertFalse(get('t1').visited('3'))
		model.Report('3', '1', '13:00')
		self.assertTrue(get('t1').completed())
		self.assertTrue(get('b3').done())

	def testTeam4Finishing(self):
		self.assertFalse(get('t4').visited('1'))
		model.Report('1', '4', '13:00')
		self.assertTrue(get('t4').completed())
		self.assertTrue(get('b1').done())

	def testTeamOnRoute(self):
		t = model.Team('testonroute', '1')
		self.assertTrue(t.on_route())

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(Testing)

if __name__ == '__main__':
	start('test')
	exec(open('test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import system
	system('rm test.hike')
