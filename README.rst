.. image:: https://travis-ci.org/NOhs/pytest-easyMPI.svg?branch=master
    :target: https://travis-ci.org/NOhs/pytest-easyMPI

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT

.. image:: https://app.codacy.com/project/badge/Grade/23f4495e7d19402f93aa29b92885f281
    :target: https://www.codacy.com/gh/NOhs/pytest-easyMPI/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NOhs/pytest-easyMPI&amp;utm_campaign=Badge_Grade


Welcome to the pytest-easyMPI package!
==================================

This package aims at making MPI code testing as similar to testing
regular serial code as possible. In doing so hopefully the users of
this plugin can focus more on writing tests of their MPI code and spend
less time figuring out how to integrate MPI tests into their other test
cases.

Short example
-------------

The following shows an example of how to combine a serial and a parallel
test in a single test file. The parallel test is run using 4 MPI ranks:

.. code:: python

    from pytest_easyMPI import mpi_parallel

    def test_serial():
        assert True

    @mpi_parallel(4)
    def test_parallel():
        # Import MPI only inside the test that needs it
        # (to avoid spawning too many MPI communicators)
        from mpi4py import MPI

        data = MPI.COMM_WORLD.gather(MPI.COMM_WORLD.Get_rank())
        if MPI.COMM_WORLD.Get_rank() == 0:
            assert sum(range(MPI.COMM_WORLD.Get_size())) == sum(data)

The test can then be run by calling::

    pytest
