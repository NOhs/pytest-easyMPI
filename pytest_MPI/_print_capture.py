import sys
import warnings
from argparse import ArgumentParser

import pytest

from mpi4py import MPI

from ._plugin import MPI_SESSION_ARGUMENT
from ._test_name_converter import get_filename

parser = ArgumentParser()
parser.add_argument("test_name")

args = parser.parse_args()

sys.stdout = open(f"{get_filename(args.test_name)}_{MPI.COMM_WORLD.Get_rank()}", "w")

return_code = pytest.main(
    [
        "--color=yes",
        MPI_SESSION_ARGUMENT,
        args.test_name,
        "-W ignore::pytest.PytestAssertRewriteWarning",
    ]
)

sys.exit(return_code)
