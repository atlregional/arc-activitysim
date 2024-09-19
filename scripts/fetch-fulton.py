from pathlib import Path
from activitysim.examples.external import download_external_example

if __name__ == "__main__":
    example_dir = download_external_example(
        name=".",
        working_dir=Path.cwd(),
        assets={
            "arc-fulton-data.tar.zst": {
                "url": "https://github.com/atlregional/arc-activitysim/releases/download/v1.3.0/arc-fulton-data.tar.zst",
                "sha256": "402c3cf1fdd96ae0342f17146453b713602ca8454b78f1e8ff8cbc403e03441e",
                "unpack": "arc-fulton-data",
            },
        },
    )
    if example_dir.joinpath("arc-fulton-data").exists():
        example_dir.joinpath("arc-fulton-data").joinpath(".gitignore").write_text(
            "**\n"
        )
