import unittest
from calculator import calculate_discount

class TestCalculator(unittest.TestCase):
    def test_member_expensive_item(self):
        # Tests when is_member is True AND price > 100
        result = calculate_discount(150, True)
        self.assertEqual(result, 150 * 0.85)  # 15% total discount

if __name__ == '__main__':
    unittest.main()
