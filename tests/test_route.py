#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest

class TestRoute(unittest.TestCase):
	def setUp(self):
		start('tests/test')

	def tearDown(self):
		elixir.session.close()

	def testEnd(self):
		b = model.Base('testend', '000000')
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
		d01 = b0.distance(b1)
		d13 = b1.distance(b3)
		along = r.distgain_from('0',b3)['dist']
		self.assertEqual(d01+d13, along)

	def testDistFromOther(self):
		r = get('r1')
		d1 = r.distgain_from('0')['dist']
		d2 = r.distgain_from('0', get('b1'))['dist']
		self.assertEqual(d1, d2)

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestRoute)

if __name__ == '__main__':
	start('tests/test')
	exec(open('tests/test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import remove
	remove('tests/test.hike')
