![main](https://github.com/ahemmershift/lazyk/actions/workflows/python.yml/badge.svg)
# lazyk
A C++/Python library for efficiently iterating over high-probability label-assignments.

## Installation
The library can be installed by cloning it and installing the Python package using pip.

```bash
git clone git@github.com:ArthurDevNL/lazyk.git
cd lazyk
pip install -e .
```

## Usage
The library can be used to iterate over the high-probability label-assignments of a given probability matrix. The following example shows how to use the library to iterate over the high-probability label-assignments of a 3x3 grid.

```python
from lazyk import lazyk
import numpy as np

probs = np.arange(1, 10).reshape(3, -1)
probs = probs / probs.sum(axis=1, keepdims=True)

for seq in lazyk(probs, cache_assignments=True): # cache_assignments is true by default, but can be turned off
    print(seq)
```

The `cache_assignments` parameter indicates whether the algorithm should cache the intermediate label-assignments. This will improve the running speed of the algorithm but also require more memory. The default value is `True` but can be turned off if memory is a concern.
