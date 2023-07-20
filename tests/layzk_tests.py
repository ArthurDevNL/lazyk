import unittest
from lazyk import lazyk
import numpy as np


class TestLazyk(unittest.TestCase):
    def test(self):
        x = np.arange(1, 49).reshape(4, -1)
        i = 0
        for _ in lazyk(x):
            i += 1
            # print(seq)
        self.assertEqual(i, 20736)


if __name__ == '__main__':
    unittest.main()
