#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest

class TestBase(unittest.TestCase):
	def setUp(self):
		start('tests/test')

	def tearDown(self):
		db.session.close()

	def testDone(self):
		self.assertTrue(get('b0').done())
		self.assertFalse(get('b1').done())
		self.assertTrue(get('b2').done())
		self.assertFalse(get('b3').done())

	def testWiggleFactor(self):
		wf1 = 1.5
		wf2 = 3.0
		conf().wfact = wf1
		d1 = Leg.get('0','1').dist
		conf().wfact = wf2
		d2 = Leg.get('0','2').dist
		self.assertEqual(float(d2)/d1, wf2/wf1)

	def testActiveUnknowns(self):
		self.assertFalse(get('b0').active()['unknown'])
		self.assertTrue(get('t4') in get('b1').active()['unknown'])
		self.assertEqual(get('b3').active()['unknown'][0], get('t1'))

	def testActive(self):
		self.assertEqual(get('b0').active()['open'], get('b0').active()['close'])
		self.assertEqual(mkdt('12:00'), get('b0').active()['open'])
		self.assertEqual(get('b2').active()['close'], mkdt('12:45'))
		self.assertEqual(get('b3').active()['open'], mkdt('12:15'))

	def testActiveRange(self):
		db.session.close()
		start('tests/temp')
		from convert import load
		load('tests/test.conf')
		exp_open = mkdt('08:13')
		exp_close = mkdt('09:57')
		t = get('b2').active(20, 60)
		self.assertEqual(t['open'], exp_open)
		self.assertEqual(t['close'], exp_close)
		self.assertFalse(t['unknown'])
		from os import remove
		remove('tests/temp.hike')

	def testRef(self):
		self.assertEqual(get('b0').ref(), '000000')
		self.assertEqual(get('b1').ref(), '000010')
		self.assertEqual(get('b3').ref(), '010010')

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestBase)

if __name__ == '__main__':
	start('tests/test')
	exec(open('tests/test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import remove
	remove('tests/test.hike')
