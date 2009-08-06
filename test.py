#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest

class Testing(unittest.TestCase):
	def setUp(self):
		start('test')
		execfile('test.reports')

	def tearDown(self):
		session.close()
		from os import system
		system('rm test.hike')

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

	def testTeamCompleted(self):
		self.assertFalse(get('t1').completed())
		self.assertTrue(get('t2').completed())
		self.assertTrue(get('t3').completed())
		self.assertFalse(get('t4').completed())

	def testTeam1Finishing(self):
		self.assertEqual(get('t1').visited('3'), [])
		Report('3', '1', '13:00')
		self.assertTrue(get('t1').completed())
		self.assertTrue(get('b3').done())

	def testTeam4Finishing(self):
		self.assertEqual(get('t4').visited('1'), [])
		Report('1', '4', '13:00')
		self.assertTrue(get('t4').completed())
		self.assertTrue(get('b1').done())

if __name__ == '__main__':
	unittest.main()
