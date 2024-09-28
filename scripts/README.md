# ARC ActivitySim Scripts

This directory contains scripts for running ActivitySim with the ARC travel demand model.

- *fetch-fulton.py*: A script for downloading the Fulton County dataset, which is
    a subset of the full ARC dataset.  This will download and extract the necessary  
    data files into the `arc-fulton-data` directory (creating it if needed).
- *run-fulton.py*: A script for running the ARC ActivitySim model using the 
    Fulton County dataset.
- *check-fulton.py*: A script for checking the output of the ARC ActivitySim 
    model using the Fulton County dataset.
- *fulton-reference-outputs.zip*: A zip file containing reference outputs for the 
    ARC ActivitySim model using the Fulton County dataset.  This is used by the 
    `check-fulton.py` script to verify the model output.
