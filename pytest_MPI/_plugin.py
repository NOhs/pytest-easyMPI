"""
Module making commandline options available to pytest which are
necessary for mpitest.
"""


MPI_SESSION_ARGUMENT = "--in_mpi_session"
"""
Argument added to the command line arguments useable with pytest.
/cf :any:`pytest_addoption`
"""

_IN_MPI_SESSION = False
"""Indicates whether the current test is run with the mpi session argument"""


def in_mpi_session():
    """
    Return if the current test is run with the mpi session argument.

    Returns
    -------
    bool
        True if current test is run with the mpi session argument,
        False otherwise.

    """
    return _IN_MPI_SESSION


def pytest_addoption(parser):
    """
    Add option `--in_mpi_session` to commandline options of pytest.

    The default value is set to `False` so that it is
    not activated by accident.

    Arguments
    ---------
    parser : ArgumentParser
        The parser to which to add the option `in_mpi_session`

    """
    parser.addoption(
        MPI_SESSION_ARGUMENT,
        action="store_true",
        help="variable used by mpitest, to indicate that the current test is "
        "run via mpirun etc. Should not be called directly.",
    )


def pytest_configure(config):
    """
    Set `IN_MPI_SESSION` module variable based on command line options.

    Arguments
    ---------
    config : Config fixture
        The configuration from which to read the command line argument

    """
    global _IN_MPI_SESSION
    _IN_MPI_SESSION = config.getoption(MPI_SESSION_ARGUMENT)
