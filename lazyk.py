import time
from queue import PriorityQueue
from typing import Dict, Generator, Optional, Tuple

from numpy.typing import NDArray
import numpy as np


def lazyk(probs: NDArray) -> Generator[NDArray, None, None]:
    lprobs = -np.log(probs)
    lprobs_argsort_row = lprobs.argsort(axis=1)

    lprobs_sorted = np.take_along_axis(lprobs, lprobs_argsort_row, axis=1)
    diff_lprobs = np.diff(lprobs_sorted, axis=1)

    q = PriorityQueue(maxsize=0)
    visited = set()
    candidates = set()
    J = {}

    y0_argsort_indexes = tuple(np.zeros(probs.shape[0], dtype='int'))
    visited.add(y0_argsort_indexes)
    candidates.add(y0_argsort_indexes)
    q.put((0, y0_argsort_indexes))
    J = {y0_argsort_indexes: 0}
    yield to_preds(lprobs_argsort_row=lprobs_argsort_row, argsort_indexes=y0_argsort_indexes)
    # yield y0_argsort_indexes, g(lprobs, lprobs_argsort_row, y0_argsort_indexes)

    argsrt_next_diff_cache = dict()

    while not q.empty():
        yi_argsort_indexes: Tuple[int] = q.get()[1]

        # Perform the best proposed change
        yk_argsort_indexes = best_change(lprobs, diff_lprobs, J, yi_argsort_indexes, argsort_next_diff_cache=argsrt_next_diff_cache)

        visited.add(yk_argsort_indexes)
        candidates.add(yk_argsort_indexes)
        yield to_preds(lprobs_argsort_row=lprobs_argsort_row, argsort_indexes=yk_argsort_indexes)
        # yield yk_argsort_indexes, g(lprobs, lprobs_argsort_row, yk_argsort_indexes)

        # Find the next best change from yk that isn't a candidate yet
        J[yk_argsort_indexes] = 0
        ykj_argsort_indexes = best_change(lprobs, diff_lprobs, J, yk_argsort_indexes, argsort_next_diff_cache=argsrt_next_diff_cache)
        while ykj_argsort_indexes is not None and ykj_argsort_indexes in candidates:
            # print('skipped ykj')
            J[yk_argsort_indexes] += 1
            ykj_argsort_indexes = best_change(lprobs, diff_lprobs, J, yk_argsort_indexes, argsort_next_diff_cache=argsrt_next_diff_cache)
            
        # Add it if it exists
        if ykj_argsort_indexes is not None:
            candidates.add(ykj_argsort_indexes)
            ykj_score = g(lprobs, lprobs_argsort_row, ykj_argsort_indexes)
            q.put((ykj_score, yk_argsort_indexes))
            
    	# Update the item we took with the next best proposal change that isn't a candidate yet
        J[yi_argsort_indexes] += 1
        yij_argsort_indexes = best_change(lprobs, diff_lprobs, J, yi_argsort_indexes, argsort_next_diff_cache=argsrt_next_diff_cache)
        while yij_argsort_indexes is not None and yij_argsort_indexes in candidates:
            # print('skipped yij')
            J[yi_argsort_indexes] += 1
            yij_argsort_indexes = best_change(lprobs, diff_lprobs, J, yi_argsort_indexes, argsort_next_diff_cache=argsrt_next_diff_cache)

        if yij_argsort_indexes is not None:
            candidates.add(yij_argsort_indexes)
            yij_score = g(lprobs, lprobs_argsort_row, yij_argsort_indexes)
            q.put((yij_score, yi_argsort_indexes))

def g(lprobs: NDArray, lprobs_argsort_row: NDArray, argsort_indexes: Tuple[int]) -> float:
    indexes = np.array(argsort_indexes)
    lprobs_indexes = np.take_along_axis(lprobs_argsort_row, indexes.reshape(-1,1), axis=1)
    logp = np.take_along_axis(lprobs, lprobs_indexes.reshape(-1,1), axis=1).sum()
    return logp
    

def best_change(lprobs: NDArray,
                diff_lprobs: NDArray,
                J: Dict[Tuple[int], int],
                argsort_indexes: Tuple[int],
                argsort_next_diff_cache: Dict[Tuple, NDArray]) -> Optional[Tuple[int]]:
    
    if J[argsort_indexes] > diff_lprobs.shape[0]:
        return None
    
    np_argsort_indexes = np.array(argsort_indexes)
    mask = np_argsort_indexes < diff_lprobs.shape[1]

    if J[argsort_indexes] == mask.sum():
        return None

    # Get or precompute the next best changes for this state
    argsrt_next_diffs = argsort_next_diff_cache.get(argsort_indexes, None)
    if argsrt_next_diffs is None:
        np_argsort_indexes[~mask] = 0
        next_diffs = np.take_along_axis(diff_lprobs, np_argsort_indexes.reshape(-1,1), axis=1).reshape(-1)
        next_diffs[~mask] = np.inf

        argsrt_next_diffs = next_diffs.argsort()
        argsort_next_diff_cache[argsort_indexes] = argsrt_next_diffs

    i_token_change = argsrt_next_diffs[J[argsort_indexes]]

    np_argsort_indexes[~mask] = diff_lprobs.shape[1]
    np_argsort_indexes[i_token_change] += 1
    return tuple(np_argsort_indexes)

def to_preds(lprobs_argsort_row: NDArray, argsort_indexes: Tuple[int]) -> NDArray:
    return np.take_along_axis(
        lprobs_argsort_row,
        np.array(argsort_indexes).reshape(-1, 1),
        axis=1,
    ).reshape(-1)


if __name__ == '__main__':
    import cProfile

    with cProfile.Profile(subcalls=True, builtins=False) as pr:
        probs = np.arange(1,37).reshape(6, -1)
        print(probs.shape[1])
        # probs = np.exp(-np.array([1,2,3]*3).reshape(3, -1))
        probs = probs / probs.sum(axis=1, keepdims=True)
        lprobs = -np.log(probs)
        last = 0
        solutions = set()

        # Time the running time of the for loop
        start = time.time()
        for seq in lazyk(probs):
            # seq = t[0]
            if tuple(seq) in solutions:
                raise ValueError("Duplicate solution")
            solutions.add(tuple(seq))

            val = np.take_along_axis(lprobs, seq.reshape(-1,1), axis=1).sum()
            # val = t[1]
            print(f"[{','.join([str(x) for x in seq])}] {val:.3f}")
            if last > val and not np.isclose(last, val, atol=1e-6):
                raise ValueError
            else:
                last = val
        pr.dump_stats('lazyk.prof')

    num_expected_solutions = probs.shape[1]**probs.shape[0]
    print(f'Found {len(solutions)}/{num_expected_solutions} solutions')
    print(f'Took {time.time() - start:.5f}s')

    print()
    print('Missing solutions:')
    # Get all possible combinations of the indexes using itertools
    import itertools
    all_combinations = itertools.product(range(probs.shape[1]), repeat=probs.shape[0])

    # Check which combinations arent in the set of solutions
    missing_solutions = set(all_combinations).difference(solutions)

    # Print each solution
    for s in missing_solutions:
        print(f"[{','.join([str(x) for x in s])}] {np.take_along_axis(lprobs, np.array(s).reshape(-1,1), axis=1).sum():.3f}")
