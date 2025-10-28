[<img src="http://gpkit.rtfd.org/en/latest/_images/gplogo.png" width=110 alt="GPkit" />](http://gpkit.readthedocs.org/)

**[Documentation](http://gpkit.readthedocs.org/)** | [Install instructions](http://gpkit.readthedocs.org/en/latest/installation.html) | [Examples](http://gpkit.readthedocs.org/en/latest/examples.html) | [Glossary](https://gpkit.readthedocs.io/en/latest/autodoc/gpkit.html) | [Citing GPkit](http://gpkit.readthedocs.org/en/latest/citinggpkit.html)

GPkit is a Python package for defining and manipulating
geometric programming models,
abstracting away the backend solver.
Supported solvers are
[mosek](http://mosek.com)
and [cvxopt](http://cvxopt.org/).

## System Requirements

GPkit requires Python 2.7-3.5 and is compatible with NumPy 1.8-1.12 and SciPy 0.15-0.19. For optimal performance, use with Mosek 7.x or 8.x solver versions.

## Usage Example
```python
from gpkit import VectorVariable, Model
import gpkit.tools.docstring as gpkitdoc
```

[![Build Status](https://acdl.mit.edu/csi/buildStatus/icon?job=CE_gpkit_Push_unit_tests)](https://acdl.mit.edu/csi/view/convex%20engineering/job/CE_gpkit_Push_unit_tests/) Unit tests

[![Build Status](https://acdl.mit.edu/csi/buildStatus/icon?job=CE_gpkit_Install)](https://acdl.mit.edu/csi/view/convex%20engineering/job/CE_gpkit_Install/) pip install

[![Build Status](https://acdl.mit.edu/csi/buildStatus/icon?job=CE_gpkit_Push_dependency_tests)](https://acdl.mit.edu/csi/view/convex%20engineering/job/CE_gpkit_Push_dependency_tests/) Dependencies