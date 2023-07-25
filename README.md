![main](https://github.com/ahemmershift/lazyk/actions/workflows/python.yml/badge.svg)
# lazyk
A C++/Python library for efficiently iterating over high-probability label-assignments.

## Installation
The library can be installed by cloning it and installing the Python package using pip.

```bash
git clone git@github.com:AHemmerShift/lazyk.git
cd lazyk
pip install -e .
```

## Usage
The library can be used to iterate over the high-probability label-assignments of a given probability matrix. The following example shows how to use the library to iterate over the high-probability label-assignments of a 3x3 grid.

```python
from lazyk import Lazyk
import numpy as np

probs = np.arange(1, 10).reshape(3, -1)
probs = probs / probs.sum(axis=1, keepdims=True)

for seq in Lazyk(probs):
    print(seq)
```
