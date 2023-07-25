import unittest
import numpy as np
from lazyk import Lazyk

class TestLazyk(unittest.TestCase):
    def test(self):
        probs = np.arange(1, 49).reshape(4, -1)
        probs = probs / probs.sum(axis=1, keepdims=True)
        lprobs = -np.log(probs)
    
        i = 0
        last_val = 0
        for seq in Lazyk(probs):
            i += 1
            
            val = np.take_along_axis(lprobs, seq.reshape(-1,1), axis=1).sum()
            # last_val <= val with 1e-10 tolerance
            self.assertTrue(last_val <= val + 1e-10)
            last_val = val
        self.assertEqual(i, 20736)


if __name__ == '__main__':
    unittest.main()
