# Python SDK

## Requirements

### With Mu Editor

None! Just download and install [Mu Editor](https://codewith.mu/).

### Without Mu Editor

- [Python 3.7.0](https://www.python.org/downloads/) or higher
- [Pip 18.0](https://pip.pypa.io/en/stable/installing/) or higher (comes installed if you download Python from [python.org](https://www.python.org/downloads/))
- [pyserial 3.4](https://pypi.org/project/pyserial/) or higher

## Installing and running examples

### With Mu Editor

1. [Download the source files](https://github.com/KanoComputing/community-sdk/archive/python.zip) and unzip it (we recommend unzipping it to `mu_code` in your home folder)
1. Open Mu Editor
1. Switch to Python3 mode
1. Load an example from `community-sdk-python/examples`:
    - For Motion Sensor `msk_all.py`
    - For Pixel Kit `rpk_stream_frame.py`
1. Press the "Run" button on Mu's toolbar.

### Without Mu Editor

1. Clone this repository: `git clone git@github.com:KanoComputing/community-sdk.git`
1. Navigate to folder: `cd community-sdk`
1. Checkout to `python` branch: `git checkout python`
1. Install dependencies: `pip install pyserial`
1. Run an example:
    - For Motion Sensor `python examples/msk_all.py`
    - For Pixel Kit `python examples/rpk_stream_frame.py`
