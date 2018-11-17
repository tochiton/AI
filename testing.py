import unittest
import hexapawn


class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(hexapawn.valid_position(3, 0, 1), True)


if __name__ == '__main__':
    unittest.main()



