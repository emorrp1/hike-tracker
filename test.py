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

assert b0.next(r1) is b1
assert b1.next('1') is b3
assert b3.next(r1) is b2
assert b2.next('1') is None
assert b0.next(r2) is b2
assert b2.next('2') is b3
assert b3.next(r2) is None

assert t1.completed() is False
assert t2.completed() is True
assert t3.completed() is True
assert t4.completed() is False

assert t1.visited('3') == []
Report(b3, t1, '13:00')
assert t1.completed() is True
assert b3.done() is True

assert t4.visited(b1) == []
Report(b1, '4', '13:00')
assert t4.completed() is True
assert b1.done() is True
