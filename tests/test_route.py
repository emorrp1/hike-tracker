#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest

class TestRoute(unittest.TestCase):
	def setUp(self):
		start('tests/test')

	def tearDown(self):
		elixir.session.close()

	def testEnd(self):
		b = Base('testend', '000000')
		r = get('r1')
		r.bases.append(b)
		self.assertEqual(b, r.end())

	def testLen(self):
		r = get('r1')
		start = r.bases[0]
		length = r.distgain_from(start, r.end())['dist']
		self.assertEqual(length, len(r))

	def testDistFrom(self):
		r = get('r1')
		b0 = get('b0')
		b1 = get('b1')
		b3 = get('b3')
		d01 = Leg.get(b0,b1).dist
		d13 = Leg.get(b1,b3).dist
		along = r.distgain_from('0',b3)['dist']
		self.assertEqual(d01+d13, along)

	def testDistFromOther(self):
		r = get('r1')
		d1 = r.distgain_from('0')['dist']
		d2 = r.distgain_from('0', get('b1'))['dist']
		self.assertEqual(d1, d2)

	def testNext1(self):
		r = get('r1')
		self.assertEqual(r.next('0'), get('b1'))
		self.assertEqual(r.next('1'), get('b3'))
		self.assertEqual(r.next('3'), get('b2'))
		self.assertEqual(r.next('2'), None)

	def testNext2(self):
		r = get('r2')
		self.assertEqual(r.next('0'), get('b2'))
		self.assertEqual(r.next('2'), get('b3'))
		self.assertFalse(r.next('3'))

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestRoute)

if __name__ == '__main__':
	start('tests/test')
	exec(open('tests/test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import remove
	remove('tests/test.hike')
