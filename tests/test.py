#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest

class Testing(unittest.TestCase):
	def setUp(self):
		start('test')

	def tearDown(self):
		elixir.session.close()

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
	import test_base
	testing = unittest.TestLoader().loadTestsFromTestCase(Testing)
	base_suite = test_base.suite()
	return unittest.TestSuite([testing, base_suite])

if __name__ == '__main__':
	start('test')
	exec(open('test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import system
	system('rm test.hike')
