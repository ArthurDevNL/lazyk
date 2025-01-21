import unittest
import numpy as np
from lazyk import lazyk

class TestLazyk(unittest.TestCase):
    
    def perform(self, n_rows, n_cols, cache_assignments=True, stop_at=None):
        # probs = np.random.rand(n_rows, n_cols)
        probs = np.arange(1, n_rows*n_cols+1).reshape(n_rows, n_cols)
        probs = probs / probs.sum(axis=1, keepdims=True)
        lprobs = -np.log(probs)

        i = 0
        last_val = 0
        seqs = []
        for seq in lazyk(probs, cache_assignments=cache_assignments):
            i += 1
            
            val = np.take_along_axis(lprobs, seq.reshape(-1,1), axis=1).sum()

            # last_val <= val with 1e-10 tolerance
            self.assertTrue(last_val <= val + 1e-10)
            seqs.append(seq)
            last_val = val

            if stop_at is not None and i >= stop_at:
                break
        if stop_at is None:
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

        # Very large with early stopping
        self.perform(45, 365, stop_at=2048)
        self.perform(365, 45, stop_at=2048)

    def test_no_cache(self):
        self.perform(2, 2, cache_assignments=False)
        self.perform(2, 2, cache_assignments=False)
        self.perform(2, 2, cache_assignments=False)

        self.perform(2, 3, cache_assignments=False)
        self.perform(3, 2, cache_assignments=False)

        # Try a bigger one: 5^7 = 78125
        self.perform(7, 5, cache_assignments=False)

        # Very large with early stopping
        self.perform(45, 365, cache_assignments=False, stop_at=2048)
        self.perform(365, 45, cache_assignments=False, stop_at=2048)
    
    def test_single_row_col(self):
        self.perform(1, 2)
        self.perform(1, 3)
        self.perform(1, 5)

        self.perform(2, 1)
        self.perform(3, 1)
        self.perform(5, 1)

if __name__ == '__main__':
    unittest.main()