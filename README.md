# XJS

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
2.  make a map of your colors, and treat that as a class, vs. your structure on 105 and 128
3.  Look into click for arg parsing
4.  Use black
5.  Add interfaces table
6.  Add sosreport handling
7.  Add sorting
8.  Date Verification
9.  Make Snap
10.  Test with v1 code
11.  Add json support
12.  Enforce pycodestyle checks
13.  Update Usage statement
13.  Fix Colors
