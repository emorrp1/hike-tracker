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
