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

assert t1.visited('3') == []
Report(b3, t1, '13:00')
assert t1.completed() is True
assert b3.done() is True

assert t4.visited(b1) == []
Report(b1, '4', '13:00')
assert t4.completed() is True
assert b1.done() is True
