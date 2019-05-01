#!/usr/bin/env python

import setuptools

setuptools.setup(
    setup_requires=["pbr", "pytest-runner"],
    tests_require=["mpi4py", "pytest"],
    entry_points={"pytest11": ["pytest-MPI = pytest_MPI._plugin"]},
    pbr=True,
)
