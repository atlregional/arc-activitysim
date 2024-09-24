import pandas as pd
import zipfile
import argparse
import os


def compare_table_artifact(
    filename="final_households.csv", artifact_name="legacy-outputs.zip"
):
    with zipfile.ZipFile("fulton-reference-outputs.zip") as z:
        with z.open(filename) as f:
            ref_tab = pd.read_csv(f)
    with zipfile.ZipFile(artifact_name) as z:
        with z.open(filename) as f:
            check_tab = pd.read_csv(f)
    try:
        pd.testing.assert_frame_equal(ref_tab, check_tab)
    except AssertionError:
        print(f"ERROR: {filename} from {artifact_name} does not match")
        raise
    else:
        print(f"OK: {filename} from {artifact_name} matches")


def compare_table_raw(filename="final_households.csv", check_dir="."):
    with zipfile.ZipFile("fulton-reference-outputs.zip") as z:
        with z.open(filename) as f:
            ref_tab = pd.read_csv(f)
    with z.open(os.path.join(check_dir, filename)) as f:
        check_tab = pd.read_csv(f)
    try:
        pd.testing.assert_frame_equal(ref_tab, check_tab)
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
        compare_table_raw("final_households.csv", args.check_dir)
        compare_table_raw("final_persons.csv", args.check_dir)
        compare_table_raw("final_tours.csv", args.check_dir)
        compare_table_raw("final_trips.csv", args.check_dir)
        compare_table_raw("final_accessibility.csv", args.check_dir)
        compare_table_raw("final_joint_tour_participants.csv", args.check_dir)
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
