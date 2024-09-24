import pandas as pd
import zipfile


def compare_table(filename="final_households.csv", artifact_name="legacy-outputs.zip"):
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


def main():
    compare_table("final_households.csv", "legacy-outputs.zip")
    compare_table("final_persons.csv", "legacy-outputs.zip")
    compare_table("final_tours.csv", "legacy-outputs.zip")
    compare_table("final_trips.csv", "legacy-outputs.zip")
    compare_table("final_accessibility.csv", "legacy-outputs.zip")
    compare_table("final_joint_tour_participants.csv", "legacy-outputs.zip")

    compare_table("final_households.csv", "sharrow-outputs.zip")
    compare_table("final_persons.csv", "sharrow-outputs.zip")
    compare_table("final_tours.csv", "sharrow-outputs.zip")
    compare_table("final_trips.csv", "sharrow-outputs.zip")
    compare_table("final_accessibility.csv", "sharrow-outputs.zip")
    compare_table("final_joint_tour_participants.csv", "sharrow-outputs.zip")


if __name__ == "__main__":
    main()
