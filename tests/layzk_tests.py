import unittest
from lazyk import lazyk
import numpy as np


class TestLazyk(unittest.TestCase):
    def test(self):
        probs = np.arange(1, 49).reshape(4, -1)
        probs = probs / probs.sum(axis=1, keepdims=True)
        lprobs = -np.log(probs)
    
        i = 0
        last_val = 0
        for seq in lazyk(probs):
            i += 1
            
            val = np.take_along_axis(lprobs, seq.reshape(-1,1), axis=1).sum()
            self.assertLessEqual(last_val, val)
            last_val = val
        self.assertEqual(i, 20736)


if __name__ == '__main__':
    unittest.main()
