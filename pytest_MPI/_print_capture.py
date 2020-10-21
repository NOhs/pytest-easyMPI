"""
Wrapper for MPI calls.

This script is called to run pytest in an MPI session and
pipe all output to files that are later gathered from all
MPI threads.
"""

import sys
from argparse import ArgumentParser

import pytest

from mpi4py import MPI

from ._plugin import MPI_SESSION_ARGUMENT
from ._mpi_test_parser import temp_ouput_file, END_OF_TEST

parser = ArgumentParser()
parser.add_argument("test_name")

args = parser.parse_args()

sys.stdout = open(f"{temp_ouput_file(args.test_name)}_{MPI.COMM_WORLD.Get_rank()}", "w")

return_code = pytest.main(
    [
        "--color=yes",
        MPI_SESSION_ARGUMENT,
        args.test_name,
        "-W ignore::pytest.PytestAssertRewriteWarning",
    ]
)

print(END_OF_TEST, end="")

sys.exit(return_code)
