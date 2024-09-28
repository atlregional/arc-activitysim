import pandas as pd
import zipfile
import argparse
import os
import pathlib
from pandas.api.types import is_float_dtype
import numpy as np

reference_outputs = pathlib.Path(__file__).parent.joinpath(
    "fulton-reference-outputs.zip"
)

DEFAULT_TOL = dict(rtol=1.0e-3, atol=1.0e-6)


def assert_frame_equal(df1, df2, sort_col=None, ignore_cols=None):
    ignore_cols = ignore_cols or []
    if sort_col is not None:
        df1 = df1.sort_values(sort_col).set_index(sort_col)
        df2 = df2.sort_values(sort_col).set_index(sort_col)
    pd.testing.assert_index_equal(df1.index, df2.index)
    error_cols = [
        "household_id",
        "person_id",
        "tour_id",
        "trip_id",
        "zone_id",
        "participant_id",
    ]
    error_cols = [c for c in error_cols if c in df1.columns]

    for k in df1.columns:
        if k in ignore_cols:
            continue
        s1 = df1[k]
        if k not in df2.columns:
            raise AssertionError(f"Column {k!r} not found in second DataFrame")
        s2 = df2[k]

        # print(f"---------- {k} ---------")
        # print("s1=", s1.iloc[:3])
        # print("s2=", s2.iloc[:3])

        if is_float_dtype(s1):
            y = np.isclose(s1.values, s2.values, equal_nan=True, **DEFAULT_TOL)
            # print("$$$\n", y)
            misses = np.where(~y)
        else:
            y = ~((s1.values == s2.values) | (s1.isna() & s2.isna()))
            misses = np.where(y)
        misses = misses[0]
        if len(misses) > 0:
            print(f"- Column {k!r} has {len(misses)} discrepancies: {misses}")
            print(
                f"- Column {k!r} left failures=\n{df1[error_cols+[k]].iloc[misses[:3]]}"
            )
            print(
                f"- Column {k!r} right failures=\n{df2[error_cols+[k]].iloc[misses[:3]]}"
            )
        if len(misses) > len(df1) * 0.01:
            pd.testing.assert_series_equal(s1, s2, check_dtype=False, **DEFAULT_TOL)
            raise AssertionError(f"Column {k!r} has {len(misses)} discrepancies")


def compare_table_artifact(
    filename="final_households.csv",
    artifact_name="legacy-outputs.zip",
    sort_col=None,
    **kwargs,
):
    with zipfile.ZipFile(reference_outputs) as z:
        with z.open(filename) as f:
            ref_tab = pd.read_csv(f)
    with zipfile.ZipFile(artifact_name) as z:
        with z.open(filename) as f:
            check_tab = pd.read_csv(f)
    try:
        assert_frame_equal(ref_tab, check_tab, sort_col, **kwargs)
    except AssertionError:
        print(f"ERROR: {filename} from {artifact_name} does not match")
        raise
    else:
        print(f"OK: {filename} from {artifact_name} matches")


def compare_table_raw(
    filename="final_households.csv", check_dir=".", sort_col=None, **kwargs
):
    with zipfile.ZipFile(reference_outputs) as z:
        with z.open(filename) as f:
            ref_tab = pd.read_csv(f)
    with open(os.path.join(check_dir, filename)) as f:
        check_tab = pd.read_csv(f)
    try:
        assert_frame_equal(ref_tab, check_tab, sort_col, **kwargs)
    except AssertionError:
        print(f"ERROR: {check_dir}/{filename} does not match")
        raise
    else:
        print(f"OK: {check_dir}/{filename} matches")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check-dir", help="directory containing output files to check", type=str
    )
    args = parser.parse_args()

    if args.check_dir:
        compare_table_raw("final_households.csv", args.check_dir, "household_id")
        compare_table_raw("final_persons.csv", args.check_dir, "person_id")
        compare_table_raw("final_tours.csv", args.check_dir, "tour_id")
        compare_table_raw("final_trips.csv", args.check_dir, "trip_id")
        compare_table_raw(
            "final_joint_tour_participants.csv",
            args.check_dir,
            sort_col="participant_id",
        )
        compare_table_raw("final_accessibility.csv", args.check_dir, sort_col="zone_id")
        return

    compare_table_artifact("final_households.csv", "legacy-outputs.zip")
    compare_table_artifact("final_persons.csv", "legacy-outputs.zip")
    compare_table_artifact("final_tours.csv", "legacy-outputs.zip")
    compare_table_artifact("final_trips.csv", "legacy-outputs.zip")
    compare_table_artifact("final_accessibility.csv", "legacy-outputs.zip")
    compare_table_artifact("final_joint_tour_participants.csv", "legacy-outputs.zip")

    compare_table_artifact("final_households.csv", "sharrow-outputs.zip")
    compare_table_artifact("final_persons.csv", "sharrow-outputs.zip")
    compare_table_artifact("final_tours.csv", "sharrow-outputs.zip")
    compare_table_artifact("final_trips.csv", "sharrow-outputs.zip")
    compare_table_artifact("final_accessibility.csv", "sharrow-outputs.zip")
    compare_table_artifact("final_joint_tour_participants.csv", "sharrow-outputs.zip")


if __name__ == "__main__":
    main()
