from pytest_MPI import mpi_parallel

@mpi_parallel(4)
def test_me():
    from mpi4py import MPI

    data = MPI.COMM_WORLD.gather(MPI.COMM_WORLD.Get_rank())
    if MPI.COMM_WORLD.Get_rank() == 0:
        assert sum(range(MPI.COMM_WORLD.Get_size())) == sum(data)
