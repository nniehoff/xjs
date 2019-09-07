# XJS

[![Snap Status](https://build.snapcraft.io/badge/nniehoff/xjs.svg)](https://build.snapcraft.io/user/nniehoff/xjs)
[![Build Status](https://travis-ci.org/nniehoff/xjs.svg?branch=master)](https://travis-ci.org/nniehoff/xjs)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/nniehoff/xjs.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/nniehoff/xjs/alerts/)

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
Usage: xjs [OPTIONS] <status files>

  xjs parses a juju status yaml/json and displays the information in a user
  friendly form highlighting specific fields of specific interest.

Options:
  --application <application name>
                                  Show only the application with the specified
                                  name
  --controller <controller name>  Show only the controller with the specified
                                  name
  -h, --hide-scale-zero           Hide applications with a scale of 0
  -s, --hide-subordinate-units    Hide subordinate units
  -c, --include-containers        Include Container information
  --machine <machine name>        Show only the machine with the specified
                                  name
  --model <model name>            Show only the model with the specified name
  --no-color                      Remove color from output
  --offline                       Don't query jujucharms.com for version
                                  information
  -a, --show-apps                 Show application information
  -m, --show-machines             Show machine information
  -d, --show-model                Show model information
  -n, --show-net                  Show network interface information
  -u, --show-units                Show unit information
  --subordinate <subordinate name>
                                  Show only the subordinate unit with the
                                  specified name
  --unit <unit name>              Show only the unit with the specified name
  --help                          Show this message and exit.
```

## TODO

1.  ~~Comment Code~~
1.  make a map of your colors, and treat that as a class, vs. your structure on 105 and 128
1.  ~~Look into click for arg parsing~~
1.  ~~Use black~~
1.  ~~Add interfaces table~~
1.  Add sosreport handling
1.  Juju Controller Status Handling from Mongo
1.  Add sosreport organizing
1.  Add sosreport fetching
1.  Add sosreport generation
1.  Add sorting
1.  ~~Add filtering~~
1.  Date Verification
1.  ~~Make Snap~~
1.  ~~Test with v1 code~~
1.  ~~Add json support~~
1.  ~~Enforce pycodestyle checks~~
1.  ~~Update Usage statement~~
1.  ~~Fix Colors~~
1.  ~~Add support for multiple models~~
1.  Get latest juju version
1.  ~~Get latest charm versions~~
1.  ~~Modify for OO~~
1.  ~~Add Copyright/License Info~~
1.  Handle Dates in a common place
1.  ~~Fix String Formatting~~
1.  Work on tab completion more
1.  Display relations