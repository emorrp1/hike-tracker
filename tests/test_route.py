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

	def testNext1(self):
		self.assertEqual(get('b0').next('1'), get('b1'))
		self.assertEqual(get('b1').next('1'), get('b3'))
		self.assertEqual(get('b3').next('1'), get('b2'))
		self.assertEqual(get('b2').next('1'), None)

	def testNext2(self):
		self.assertEqual(get('b0').next('2'), get('b2'))
		self.assertEqual(get('b2').next('2'), get('b3'))
		self.assertFalse(get('b3').next('2'))

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestRoute)

if __name__ == '__main__':
	start('tests/test')
	exec(open('tests/test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import remove
	remove('tests/test.hike')
