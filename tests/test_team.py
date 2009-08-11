#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest

class TestTeam(unittest.TestCase):
	def setUp(self):
		start('test')

	def tearDown(self):
		elixir.session.close()

	def testCompleted(self):
		self.assertFalse(get('t1').completed())
		self.assertTrue(get('t2').completed())
		self.assertTrue(get('t3').completed())
		self.assertFalse(get('t4').completed())

	def testT1Finishing(self):
		self.assertFalse(get('t1').visited('3'))
		model.Report('3', '1', '13:00')
		self.assertTrue(get('t1').completed())
		self.assertTrue(get('b3').done())

	def testT4Finishing(self):
		self.assertFalse(get('t4').visited('1'))
		model.Report('1', '4', '13:00')
		self.assertTrue(get('t4').completed())
		self.assertTrue(get('b1').done())

	def testOnRoute(self):
		t = model.Team('testonroute', '1')
		self.assertTrue(t.on_route())

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestTeam)

if __name__ == '__main__':
	start('test')
	exec(open('test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import system
	system('rm test.hike')
