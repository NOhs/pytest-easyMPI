Welcome to the pytest-MPI package!
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

    from pytest_MPI import mpi_parallel
    from mpi4py import MPI

    def test_serial():
        assert True

    @mpi_parallel(4)
    def test_parallel():
        data = MPI.COMM_WORLD.gather(MPI.COMM_WORLD.Get_rank())
        if MPI.COMM_WORLD.Get_rank() == 0:
            assert sum(range(MPI.COMM_WORLD.Get_size())) == sum(data)

The test can then be run by calling::

    pytest
