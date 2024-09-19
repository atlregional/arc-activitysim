import os

os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

import activitysim.abm  # register components # noqa: F401
from pathlib import Path
import sharrow

print("ActivitySim Version:", activitysim.__version__)
print("Sharrow Version:", sharrow.__version__)

from activitysim.core import workflow

def local_path(dirname):
    return os.path.join(os.path.dirname(__file__), dirname)

def main():
    out_dir = local_path("output")
    Path(out_dir).mkdir(exist_ok=True)
    Path(out_dir).joinpath(".gitignore").write_text("**\n")