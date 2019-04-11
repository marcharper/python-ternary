import unittest

from numpy.testing import assert_array_almost_equal

import ternary


def extract_labels(tax):
    labels = []
    for k, v in tax._labels.items():
        labels.append(v[0])
    return labels


class FunctionCases(unittest.TestCase):
    def test_tax(self):
        scale = 10
        fig, tax = ternary.figure(scale=scale)
        self.assertEqual(scale, tax._scale)

    def test_axis_labels(self):
        scale = 10
        fig, tax = ternary.figure(scale=scale)
        tax.right_axis_label("right")
        self.assertEqual(extract_labels(tax), ["right"])
        tax.left_axis_label("left")
        self.assertEqual(extract_labels(tax), ["right", "left"])
        tax.bottom_axis_label("bottom")
        self.assertEqual(extract_labels(tax), ["right", "left", "bottom"])


if __name__ == "__main__":
    unittest.main()
