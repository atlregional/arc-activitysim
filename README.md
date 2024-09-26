# arc-activitysim
The standalone activitysim implementation for ARC travel demand model.

## Installation

To install the ARC ActivitySim model, simply clone this repository:

```bash
git clone https://github.com/atlregional/arc-activitysim.git
cd arc-activitysim
``` 

Using this model requires ActivitySim 1.3 or later.  This is most easily
accomplished using the `activitysim` conda package, which first requires the
installation of the `conda` package manager.  For most systems, the Miniforge
distribution is recommended, which can be downloaded from 
[conda-forge](https://github.com/conda-forge/miniforge?tab=readme-ov-file#miniforge3).

Once `conda` is installed, the `activitysim` package can be installed from the 
MiniForge Prompt (or the terminal on Linux/Mac):

```bash
conda create -n ARC-ASIM activitysim -c conda-forge --override-channels
```

This will create a new conda environment named `ARC-ASIM` with the `activitysim`
package installed.  To activate the environment, use:

```bash 
conda activate ARC-ASIM
```

## Running the Model

The ARC ActivitySim model can be run using the `activitysim` command line tool.
The model is configured using the `configs` directory, which contains the
configuration files for the model.  From the directory where this repository 
has been cloned, the model can be run using the following command:

```bash
activitysim run -c configs -d data_dir -o output_dir
```

Where `data_dir` is the directory containing the input data for the model, and
`output_dir` is the directory where the model output will be written.  The data
directory should contain the necessary input files (houeholds, persons, land use,
and skims), which can be the full scale ARC data or a smaller test data set (see
instructions to access the Fulton County test data below).  The output directory
will be created if it does not exist, and the model output will be written to
subdirectories of this directory.

## Running the Model with Sharrow

The ARC ActivitySim model can also be run with the sharrow enabled.  This is
done by adding the relevant sharrow configs directory to the command.  For
example, to run the model with the sharrow in compile-test mode, use the 
following command:
    
```bash 
activitysim run -c configs -c configs_sh_compile -d data_dir -o output_dir
``` 

This will run the model with the sharrow enabled, and will compile the numba
code and run tests to ensure the results match between sharrow and legacy modes. 
Once the sharrow compiling is complete, the model can subsequently be run in
sharrow's "production" mode, which will be much faster:

```bash
activitysim run -c configs -c configs_sh -d data_dir -o output_dir
``` 

## Testing Dataset (Fulton County)

This model is built to run with the data that simulates the full-scale
model of the ARC region, but this scale of data can be overwhelming 
for testing the operation of the model, especially on more limited
platforms.

To facilitate testing, data for a smaller slice of the region is available.
This test data includes just Fulton County, which has 1,296 zones; this is
a small enough area to run the model on a laptop or within the CI testing
infrastructure, as it will require only about 6GB of RAM to to store the
skims in memory, and another 1 or 2 GB for the rest of the model. But this 
area is still large enough to provide a meaningful test of the model, with 
enough zones to exercise the model's capabilities and complexity. The Fulton 
County data can be downloaded with this Python script (also available
as [fetch-fulton.py](./scripts/fetch-fulton.py)):

```python
from pathlib import Path
from activitysim.examples.external import download_external_example

example_dir = download_external_example(
  name=".", 
  working_dir=Path.cwd(),
  assets={
    "arc-fulton-data.tar.zst": {
      "url": "https://github.com/atlregional/arc-activitysim/releases/download/v1.3.0/arc-fulton-data.tar.zst",
      "sha256": "402c3cf1fdd96ae0342f17146453b713602ca8454b78f1e8ff8cbc403e03441e",
      "unpack": "arc-fulton-data",
    },
  }
)
```

## Continuous Integration Testing

This repository is configured to run continuous integration testing
using GitHub Actions. The tests are run on a small subset of the data
for Fulton County, and the results are uploaded to the `Actions` tab
of the repository.  The tests are configured in the `.github/workflows`
directory, and use the scripts in the `scripts` directory.

Note that the tests with sharrow enabled are run in a clean environment
every time, so the sharrow test includes the overhead of compiling all
the numba code.  This will make it appear that the sharrow test is *much*
slower than the legacy test; this is normal an not an indication that 
sharrow is slower than the legacy code for production runs.
