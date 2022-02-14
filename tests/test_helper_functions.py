# Standard library imports 
from pprint import pprint
import unittest

# Local application imports
from context import helper_functions as h_func


class TestCreatures(unittest.TestCase):
    def test_span(self):
        self.assertEqual(h_func.span(2, 5), (0, 7))
        self.assertEqual(h_func.span(2, (5, 5)), (0, 7))
        self.assertEqual(h_func.span(2, 5, negative=True), (-3, 7))
        self.assertEqual(h_func.span(2, (5, 5), negative=True), (-3, 7))

        self.assertEqual(h_func.span(2, (4, 6)), (0, 8))
        self.assertEqual(h_func.span(2, (4, 6), negative=True), (-2, 8))

        self.assertEqual(h_func.span(2.4, 5), (0, 7.4))
        self.assertEqual(h_func.span(2.4, (5, 5)), (0, 7.4))
        self.assertEqual(h_func.span(2.4, 5, negative=True), (-2.6, 7.4))
        self.assertEqual(h_func.span(2.4, (5, 5), negative=True), (-2.6, 7.4))

        self.assertEqual(h_func.span(2.4, (4, 6)), (0, 8.4))
        self.assertEqual(h_func.span(2.4, (4, 6), negative=True), (-1.6, 8.4))
    
    def test_span_typeError(self):
        # Testing the first argument
        self.assertRaises(TypeError, h_func.span, "2", 2)
        self.assertRaises(TypeError, h_func.span, ["2"], 2)
        self.assertRaises(TypeError, h_func.span, {"2": 2}, 2)
        self.assertRaises(TypeError, h_func.span, (2, 2), 2)
        self.assertRaises(TypeError, h_func.span, True)

        # Testing the second argument
        self.assertRaises(TypeError, h_func.span, 2, "2")
        self.assertRaises(TypeError, h_func.span, 2, ["2"])
        self.assertRaises(TypeError, h_func.span, 2, {"2": 2})
        self.assertRaises(TypeError, h_func.span, 2, False)

        # Testing the third argument
        self.assertRaises(TypeError, h_func.span, 2, 2, 2)
        self.assertRaises(TypeError, h_func.span, 2, 2, "2")
        self.assertRaises(TypeError, h_func.span, 2, 2, [2])
        self.assertRaises(TypeError, h_func.span, 2, 2, (2, 2))
        self.assertRaises(TypeError, h_func.span, 2, 2, {'s': 2})

    def test_span_indexError(self):
        self.assertRaises(IndexError, h_func.span, 2, (6, 2, 6))
        self.assertRaises(IndexError, h_func.span, 2, (6,))

    def test_span_valueError(self):
        self.assertRaises(ValueError, h_func.span, 2, (6, "2"))
        self.assertRaises(ValueError, h_func.span, 2, (6, True))
        self.assertRaises(ValueError, h_func.span, 2, ("2", 7))
        self.assertRaises(ValueError, h_func.span, 2, (True, 7))



if __name__ == '__main__':
    unittest.main()