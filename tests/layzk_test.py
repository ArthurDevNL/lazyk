import unittest
import numpy as np
from lazyk import Lazyk

class TestLazyk(unittest.TestCase):
    
    def perform(self, n_rows, n_cols):
        # probs = np.random.rand(n_rows, n_cols)
        probs = np.arange(1, n_rows*n_cols+1).reshape(n_rows, n_cols)
        probs = probs / probs.sum(axis=1, keepdims=True)
        lprobs = -np.log(probs)

        i = 0
        last_val = 0
        seqs = []
        for seq in Lazyk(probs):
            i += 1
            
            val = np.take_along_axis(lprobs, seq.reshape(-1,1), axis=1).sum()

            # last_val <= val with 1e-10 tolerance
            self.assertTrue(last_val <= val + 1e-10)
            seqs.append(seq)
            last_val = val
        self.assertEqual(i, n_cols**n_rows)

        # Assert that all sequences are unique
        seqs = np.array(seqs)
        self.assertEqual(len(seqs), len(np.unique(seqs, axis=0)))

    def test(self):
        self.perform(2, 2)
        self.perform(3, 3)
        self.perform(5, 5)

        self.perform(2, 3)
        self.perform(3, 2)

        # Try a bigger one: 5^7 = 78125
        self.perform(7, 5)

if __name__ == '__main__':
    unittest.main()
