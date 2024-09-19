# arc-activitysim
The standalone activitysim implementation for ARC travel demand model.

## Testing Dataset

This model is built to run with the data that simulates the full-scale
model of the ARC region, but this scale of data can be overwhelming 
for testing the operation of the model, especially on more limited
platforms.

To facilitate testing, data for a smaller slice of the region (just 
Fulton County) can be downloaded with this Python script:

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
