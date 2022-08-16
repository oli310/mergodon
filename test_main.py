import unittest
from main import solution_dataframe
from datetime import datetime as dt

class TestSolutionDataFrame(unittest.TestCase):
	def test_area(self):
		self.assertAlmostEqual(solution_dataframe('1'))
		self.assertAlmostEqual(solution_dataframe(0))
		self.assertAlmostEqual(solution_dataframe(dt.now()))
	def test_values(self):
		self.assertRaises(ValueError, solution_dataframe)