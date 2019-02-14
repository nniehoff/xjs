# XJS

[![Snap Status](https://build.snapcraft.io/badge/nniehoff/xjs.svg)](https://build.snapcraft.io/user/nniehoff/xjs)

This is a tool for parsing seemingly complex juju status yaml/json files.  It
is currently still in early alpha stages of development.

## Installation

```bash
sudo apt install python3 python3-pip
pip3 install prettytable yaml
```

## Usage

```bash
./xjs.py -i input.yaml
```

TODO: There are other options that are not documented

## TODO

1.  Comment Code
1.  make a map of your colors, and treat that as a class, vs. your structure on 105 and 128
1.  Look into click for arg parsing
1.  Use black
1.  Add interfaces table
1.  Add sosreport handling
1.  Add sorting
1.  Date Verification
1.  Make Snap
1.  Test with v1 code
1.  Add json support
1.  Enforce pycodestyle checks
1.  Update Usage statement
1.  Fix Colors
1.  Add support for multiple models

