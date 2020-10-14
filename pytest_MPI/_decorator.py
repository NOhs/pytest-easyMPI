import contextlib
import functools
import operator
import os
import shutil
import subprocess
import sys

import pytest
from colorama import Fore, Style
from mpi4py import MPI

from ._plugin import in_mpi_session
from ._test_name_converter import get_filename, get_pytest_input
from ._message_parser import contains_failure, get_traceback, get_summary


def mpi_executable(preferred_executable=None):
    """Return an mpi executable found on the current system.

    Depending on your MPI implementation, the executable name
    to run an MPI application may differ. This function will
    check which one is available and return the first valid one
    it finds. Valid in this case means that it can be found with
    methods like `which`.
    To override which executable to check first you can pass
    your preferred executable as an argument.

    Parameters
    ----------
    preferred_executable : str, optional
        The first executable to check for on the system. If it
        isn't found, will continue with the regular search for
        valid MPI executables.

    Returns
    -------
    str
        The name of a valid MPI executable.

    Raises
    ------
    RuntimeError
        If no valid MPI executable could be found, a RuntimeError
        is raised.

    """
    if preferred_executable:
        if shutil.which(preferred_executable):
            return preferred_executable
        else:
            raise RuntimeError(
                f"The given preferred mpi executable `{preferred_executable}` "
                "was not found on this system"
            )

    executables = ["mpirun", "mpiexec", "srun"]
    for executable in executables:
        if shutil.which(executable):
            return executable

    raise RuntimeError(
        "Could not find an mpi installation. Make sure your PATH is set " "correctly."
    )


def mpi_parallel(nprocs: int, mpi_executable_name=None):
    """
    Decorate a test to run in an MPI environment. The test is
    spawned via::

        <mpi_executable_name> -np <nprocs> <python_executable>...

    Parameters
    ----------
    nprocs : int
        The number of mpi processes to spawn for this test.
    mpi_executable_name : str
        The mpi executable to use when spawning the mpi tests.
        By default this function uses :any:`mpi_executable`
        to find a valid mpi executable.
    """

    def dec(func):
        @functools.wraps(func)
        def replacement_func(*args, **kwargs):
            # __tracebackhide__ = True
            if not in_mpi_session():
                executable = mpi_executable(mpi_executable_name)
                test_name = get_pytest_input(func)

                failed = False

                try:
                    mpi_subprocess_output = subprocess.check_output(
                        [
                            executable,
                            "-np",
                            str(nprocs),
                            sys.executable,
                            "-m",
                            "mpi4py",
                            "-m",
                            "pytest_MPI._print_capture",
                            test_name,
                        ],
                        stderr=subprocess.STDOUT,
                        universal_newlines=True,
                    )
                except subprocess.CalledProcessError as error:
                    failed = True
                    alternative_output = error.output

                errors = []
                for i in range(nprocs):
                    file_name = f"{get_filename(test_name)}_{i}"
                    if os.path.isfile(file_name):
                        with open(file_name) as f:
                            rank_output = f.read()
                        os.remove(file_name)

                        if not contains_failure(rank_output):
                            continue

                        errors.append((i, rank_output))

                for rank, message in errors:
                    header_1 = f"Rank {rank}"
                    header_2 = f" reported an error:"
                    header = f"{Style.BRIGHT}{Fore.RED}{header_1}{Style.RESET_ALL}{header_2}"
                    print("\n" + header)
                    print("- " * (len(header_1 + header_2)//2 + 1))
                    print(get_traceback(message))

                if failed:
                    if errors:
                        pytest.fail(get_summary(message))
                    else:
                        print(alternative_output)
                        assert False


            else:
                func(*args, **kwargs)

        return replacement_func

    return dec
