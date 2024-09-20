# ruff: noqa: E402
import os

# These environment variables are set to 1 to ensure that the model runs single-threaded
# This needs to be done before ActivitySim or any other dependency is imported
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

import argparse
import activitysim.abm  # register components # noqa: F401
from pathlib import Path
import sharrow

print("ActivitySim Version:", activitysim.__version__)
print("Sharrow Version:", sharrow.__version__)

from activitysim.core import workflow


def local_path(dirname) -> str:
    return str(Path(__file__).parents[1].joinpath(dirname))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sharrow", help="use sharrow", action="store_true")
    parser.add_argument("--households-sample-size", type=int, default=1000)
    args = parser.parse_args()

    # These things change based on whether we are using sharrow or not.
    if args.sharrow:
        print("sharrow activated")
        configs_dir = (
            local_path("configs_sh_compile"),
            local_path("configs"),
        )
        out_dir = local_path("output-fulton-sharrow")
    else:
        configs_dir = local_path("configs")
        out_dir = local_path("output-fulton-legacy")

    # ensure the output directory exists, and do not commit any output to git
    Path(out_dir).mkdir(exist_ok=True)
    Path(out_dir).joinpath(".gitignore").write_text("**\n")

    # check that the arc-fulton-data has been downloaded
    if not Path(local_path("arc-fulton-data")).exists():
        raise FileNotFoundError(
            "arc-fulton-data directory not found. Please download the fulton data"
        )

    # for this test script, we will sample a limited number of households,
    # and run the model with only 2 processes.
    settings = {
        "households_sample_size": args.households_sample_size,
        "num_processes": 2,
        # user can modify other settings here if desired
    }

    # set `resume_after` to None to start from the beginning even if a partial
    # result exists, otherwise use underscore to resume from where it left off
    resume_after = "_"

    # create a state object and run the model
    state = workflow.State.make_default(
        configs_dir=configs_dir,
        data_dir=local_path("arc-fulton-data"),
        output_dir=out_dir,
        settings=settings,
        cache_dir=Path(out_dir).joinpath("cache"),
    )
    state.import_extensions([])
    state.logging.config_logger()
    state.run.all(resume_after=resume_after)


if __name__ == "__main__":
    main()
