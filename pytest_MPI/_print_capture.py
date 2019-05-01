import subprocess
import sys
from argparse import ArgumentParser

from mpi4py import MPI

from ._plugin import MPI_SESSION_ARGUMENT
from ._test_name_converter import get_filename

parser = ArgumentParser()
parser.add_argument("test_name")

args = parser.parse_args()

try:
    subprocess.check_output(
        [sys.executable, "-m", "pytest", "--color=yes", MPI_SESSION_ARGUMENT]
        + [args.test_name],
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
except subprocess.CalledProcessError as error:
    with open(
        f"{get_filename(args.test_name)}_{MPI.COMM_WORLD.Get_rank()}", "w"
    ) as f:
        test_name = args.test_name.split(":")[-1]
        output = error.output.split("\n")
        for i in range(len(output)):
            if test_name in output[i]:
                break

        output = "\n".join(output[i + 1 : -2])
        f.write(output)
    sys.exit(error.returncode)
