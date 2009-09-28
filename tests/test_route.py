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
		length = r.bases[0].distgain_along(r, r.end())['dist']
		self.assertEqual(length, len(r))

	def testDistAlong(self):
		b0 = get('b0')
		b1 = get('b1')
		b3 = get('b3')
		d01 = b0.distance(b1)
		d13 = b1.distance(b3)
		along = b0.distgain_along('1',b3)['dist']
		self.assertEqual(d01+d13, along)

	def testDistAlongOther(self):
		b0 = get('b0')
		d1 = b0.distgain_along('1')['dist']
		d2 = b0.distgain_along('1', get('b1'))['dist']
		self.assertEqual(d1, d2)

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestRoute)

if __name__ == '__main__':
	start('tests/test')
	exec(open('tests/test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import remove
	remove('tests/test.hike')
