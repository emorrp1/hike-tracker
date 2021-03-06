#!/usr/bin/env python3
from tracker import *
import unittest

class TestTeam(unittest.TestCase):
	def setUp(self):
		start('tests/test')

	def tearDown(self):
		db.session.close()

	def testMissed(self):
		self.assertTrue(get('t1').missed())
		self.assertFalse(get('t2').missed())
		self.assertEqual(get('t3').missed(), -1)
		self.assertTrue(get('t4').missed())
		self.assertEqual(get('t4').missed(), 1)

	def testT1Finishing(self):
		self.assertFalse(get('t1').visited('3'))
		Report('3', '1', '13:00')
		self.assertFalse(get('t1').missed())
		self.assertTrue(get('b3').done())

	def testT4Finishing(self):
		t = get('t4')
		self.assertFalse(t.visited('1'))
		Report('1', t, '13:00')
		Report('2', t, '13:10')
		self.assertFalse(t.missed())
		self.assertTrue(get('b1').done())

	def testOnRoute(self):
		t = Team('testonroute', '1')
		self.assertTrue(t.on_route())
		self.assertFalse(get('t1').on_route())
		self.assertTrue(get('t2').on_route())
		self.assertTrue(get('t3').on_route())

	def testStarted(self):
		t = Team('test')
		self.assertFalse(t.started())
		Report('1', t, '13:00')
		self.assertTrue(t.started())

	def testNotStartedNotFinished(self):
		Team('test')
		for t in Team.query.all():
			if not t.started():
				self.assertFalse(t.finished())

	def testVisited(self):
		self.assertTrue(get('t1').visited('1'))
		self.assertFalse(get('t1').visited('3'))
		self.assertTrue(get('t3').visited('2'))
		t = get('t2').visited('0')
		self.assertTrue(isinstance(t, datetime))
		self.assertEqual(mkdt('12:00'), t)

	def testLastVisited(self):
		lv = get('t1').last_visited()
		self.assertTrue(isinstance(lv['base'], Base))
		self.assertTrue(isinstance(lv['dep'], datetime))
		self.assertEqual(get('t1').visited(lv['base']), lv['dep'])
		t = Team('test')
		empty = {'dep':None, 'base':None}
		self.assertEqual(empty, t.last_visited())

	def testTraversed(self):
		self.assertEqual(conf().wfact, 1.3)
		t = Team('test')
		self.assertEqual(t.traversed()['dist'], 0)
		for t in Team.query.all():
			self.assertTrue(t.traversed()['dist'] >= 0)
			self.assertTrue(t.traversed()['dist'] <= 300)
		self.assertEqual(get('t2').traversed()['dist'], 39)
		self.assertEqual(get('t4').traversed()['dist'], 31)

	def testTimings(self):
		t = Team('test')
		empty = {'walking':0, 'stopped':0}
		self.assertEqual(empty, t.timings())
		for t in Team.query.all():
			ts = t.timings()
			self.assertTrue(ts['walking'] >= 0)
			self.assertTrue(ts['stopped'] >= 0)
			self.assertTrue(ts['walking'] >= ts['stopped'])

	def testSpeed(self):
		for t in Team.query.all():
			sp = t.speed()
			self.assertTrue(sp >= 0)
			self.assertTrue(sp <= 70)

	def testLate(self):
		from datetime import datetime, timedelta
		diff = timedelta(minutes=40)
		start = datetime.now() - diff
		t = Team('testing','1')
		t.start = start
		self.assertTrue(t.late(speed=30))
		self.assertFalse(t.late(diff/2, 30))
		t.start += diff/2
		self.assertFalse(t.late(speed=30))

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestTeam)

if __name__ == '__main__':
	start('tests/test')
	exec(open('tests/test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import remove
	remove('tests/test.hike')
