import os
from pathlib import Path

import pytest

from activitysim.core import workflow


def _example_path(dirname):
    """Paths to things in the top-level directory of this repository."""
    return os.path.normpath(os.path.join(os.path.dirname(__file__), "..", dirname))


def _test_path(dirname) -> Path:
    """Paths to things in the `tests` directory."""
    return Path(__file__).parent.joinpath(dirname)


EXPECTED_MODELS = [
    "initialize_landuse",
    "compute_accessibility",
    "initialize_households",
    "school_location",
    "workplace_location",
    "auto_ownership_simulate",
    "free_parking",
    "cdap_simulate",
    "mandatory_tour_frequency",
    "mandatory_tour_scheduling",
    "joint_tour_frequency",
    "joint_tour_composition",
    "joint_tour_participation",
    "joint_tour_destination",
    "joint_tour_scheduling",
    "non_mandatory_tour_frequency",
    "non_mandatory_tour_destination",
    "non_mandatory_tour_scheduling",
    "tour_mode_choice_simulate",
    "atwork_subtour_frequency",
    "atwork_subtour_destination",
    "atwork_subtour_scheduling",
    "atwork_subtour_mode_choice",
    "stop_frequency",
    "trip_purpose",
    "trip_destination",
    "trip_purpose_and_destination",
    "trip_scheduling_choice",
    "trip_departure_choice",
    "trip_mode_choice",
    "parking_location",
    "write_data_dictionary",
    "track_skim_usage",
    "write_trip_matrices",
    "write_tables",
]


@pytest.mark.parametrize("use_sharrow", [False, True])
def test_arc_progressive(use_sharrow):
    import activitysim.abm  # register components # noqa: F401

    out_dir = _test_path(
        "output-progressive-sharrow" if use_sharrow else "output-progressive"
    )
    out_dir.mkdir(exist_ok=True)
    out_dir.joinpath(".gitignore").write_text("**\n")

    settings = dict(
        cleanup_pipeline_after_run=False,
        treat_warnings_as_errors=True,
        households_sample_size=1000,
        chunk_size=0,
        use_shadow_pricing=True,
        multiprocess=False,
    )
    tags = ["-hh1000"]

    if use_sharrow:
        settings["sharrow"] = "test"
        settings["recode_pipeline_columns"] = True
        tags.append("-recode")

    state = workflow.State.make_default(
        configs_dir=(_example_path(r"configs"),),
        data_dir=_example_path("arc-fulton-data"),
        output_dir=out_dir,
        settings=settings,
    )
    state.logging.config_logger()

    assert state.settings.models == EXPECTED_MODELS
    assert state.settings.chunk_size == 0
    if not use_sharrow:
        assert not state.settings.sharrow

    tags = "".join(tags)
    ref_pipeline = Path(__file__).parent.joinpath(
        f"regress/reference-pipeline{tags}.parquetpipeline"
    )

    for step_name in EXPECTED_MODELS:
        state.run.by_name(step_name)
        if ref_pipeline.exists():
            try:
                # The usual default rtol=1e-5 is too strict for cross-platform testing
                state.checkpoint.check_against(
                    ref_pipeline, checkpoint_name=step_name, rtol=3.3e-5
                )
            except Exception:
                print(f"> {step_name}: ERROR")
                raise
            else:
                print(f"> {step_name}: ok")
        else:
            print(f"> {step_name}: ran, not checked (no reference pipeline)")

    if not ref_pipeline.exists():
        # make new reference pipeline file if it is missing
        import shutil

        if ref_pipeline.suffix == ".zip":
            shutil.make_archive(
                ref_pipeline.with_suffix(""), "zip", state.checkpoint.store.filename
            )
        else:
            shutil.copytree(state.checkpoint.store.filename, ref_pipeline)
            if (ref_pipeline / ".gitignore").exists():
                os.remove(ref_pipeline / ".gitignore")


if __name__ == "__main__":
    test_arc_progressive(use_sharrow=False)
    test_arc_progressive(use_sharrow=True)
