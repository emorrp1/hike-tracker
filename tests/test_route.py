#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
import unittest

class TestRoute(unittest.TestCase):
	def setUp(self):
		start('test')

	def tearDown(self):
		elixir.session.close()

	def testRouteEnd(self):
		b = model.Base('testend', '000000')
		r = get('r1')
		r.bases.append(b)
		self.assertEqual(b, r.end())

	def testRouteLen(self):
		r = get('r1')
		length = r.bases[0].distance_along(r, r.end())
		self.assertEqual(length, len(r))

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestRoute)

if __name__ == '__main__':
	start('test')
	exec(open('test.reports').read())
	unittest.TextTestRunner().run(suite())
	from os import system
	system('rm test.hike')
