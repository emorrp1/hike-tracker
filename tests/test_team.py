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
		self.assertFalse(get('t1').on_route())
		self.assertTrue(get('t2').on_route())
		self.assertTrue(get('t3').on_route())

	def testStarted(self):
		t = model.Team('test')
		self.assertFalse(t.started())
		model.Report('1', t, '13:00')
		self.assertTrue(t.started())

	def testNotStartedNotFinished(self):
		model.Team('test')
		for t in model.Team.query.all():
			if not t.started():
				self.assertFalse(t.finished())

	def testVisited(self):
		self.assertTrue(get('t1').visited('1'))
		self.assertFalse(get('t1').visited('3'))
		self.assertTrue(get('t3').visited('2'))
		t = get('t2').visited('0')
		self.assertEqual(type(t).__name__, 'datetime')
		self.assertEqual(model.mkdt('12:00'), t)

	def testLastVisited(self):
		lv = get('t1').last_visited()
		self.assertEqual(type(lv[0]).__name__, 'Base')
		self.assertEqual(type(lv[1]).__name__, 'datetime')
		self.assertEqual(get('t1').visited(lv[0]), lv[1])
		t = model.Team('test')
		self.assertEqual((None, None), t.last_visited())

	def testTraversed(self):
		self.assertEqual(model.Base.wfact, 1.3)
		t = model.Team('test')
		self.assertEqual(t.traversed(), 0)
		self.assertEqual(type(get('t1').traversed()).__name__, 'int')
		for t in model.Team.query.all():
			self.assertTrue(t.traversed() >= 0)
			self.assertTrue(t.traversed() <= 300)
		self.assertEqual(get('t2').traversed(), 39)
		self.assertEqual(get('t4').traversed(), 31)

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestTeam)

if __name__ == '__main__':
	start('test')
	exec(open('test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import system
	system('rm test.hike')
