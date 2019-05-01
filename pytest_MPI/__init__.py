from pbr.version import VersionInfo
from ._decorator import mpi_parallel

_v = VersionInfo("mgen").semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()
