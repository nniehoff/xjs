# XJS

[![Snap Status](https://build.snapcraft.io/badge/nniehoff/xjs.svg)](https://build.snapcraft.io/user/nniehoff/xjs)
[![Build Status](https://travis-ci.org/nniehoff/xjs.svg?branch=master)](https://travis-ci.org/nniehoff/xjs)

This is a tool for parsing seemingly complex juju status yaml/json files.  It
is currently still in early alpha stages of development.

## Installation

```bash
sudo snap install --edge xjs
```

## Usage

With yaml:
```bash
xjs -y inputfile.yaml
```

With json:
```bash
xjs -j inputfile.json
```

Options:
```
Usage: xjs [OPTIONS] STATUSFILE

  xjs parses a juju status yaml/json and displays the information in a user
  friendly form highlighting specific fields of specific interest.

Options:
  -h, --hide-scale-zero         Hide applications with a scale of 0
  -s, --hide-subordinate-units  Hide subordinate units
  -a, --show-apps               Show application information
  -u, --show-units              Show unit information
  -m, --show-machines           Show machine information
  -n, --show-net                Show network interface information
  -d, --show-model              Show model information
  -c, --include-containers      Include Container information
  --offline                     Include Container information
  --help                        Show this message and exit.
```

## TODO

1.  ~~~Comment Code~~~
1.  make a map of your colors, and treat that as a class, vs. your structure on 105 and 128
1.  ~~Look into click for arg parsing~~
1.  ~~Use black~~
1.  ~~Add interfaces table~~
1.  Add sosreport handling
1.  Add sosreport organizing
1.  Add sosreport fetching
1.  Add sosreport generation
1.  Add sorting
1.  Date Verification
1.  ~~Make Snap~~
1.  Test with v1 code
1.  ~~Add json support~~
1.  ~~Enforce pycodestyle checks~~
1.  ~~Update Usage statement~~
1.  Fix Colors
1.  Add support for multiple models
1.  Get latest juju version
1.  ~~Get latest charm versions~~
1.  ~~Modify for OO~~
1.  Add Copyright/License Info

