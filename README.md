*Warning: Everything in this repository is under active development, so it is all subject to change.*

# Builder

## Description

This repository contains:

1. Builder CLI
2. Builder Python API

## Installation

Install with the following command. You may want to prefix the command with `sudo`.

```
pip install git+https://github.com/machineeeee/builder-python
```

TODO: Allow one line install using the following pattern (similar to brew):
```
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

## Device Model File Format

Device model files need to be formatted in [[YAML]] markup. These files have the `*.yaml` extension.

An example device model file is given below (this is the same as <path>):

```
YAML device file here...
```

## Command Line Interface

### Usage

```
builder connect --model raspberry-pi-3 --model machineee/generic-servo --model ir-rangefinder --model ir-rangefinder
```

#### `builder init`

_Examples:_
```
builder init					Used to initialize this folder (assigns a default name).
builder init -v					Used to create and init a VM (via Vagrant).
builder init fiery-fox -v			Used to initialize a new VM named fiery-fox.
builder init desktop				Used to init a Builder env called desktop.
```

#### `builder start`
#### `builder stop`
#### `builder announce`
#### `builder manage`

#### `builder device`
##### `builder device list|add|remove`

#### `builder interface`
#### `builder view`

**Unorganized**

```
signup
login
help
note [add|remove|list]		Used to add, remove, or list notes for a device or environment/workspace/project.
assemble			Starts interactive self-assembly.
start [broadcast|discover]
status [broadcast|discover]
run [broadcast|discover]
stop [broadcast|discover]
monitor [broadcast|discover]

log
```
## API

This repository contains the Python API.

### Usage

Coming soon!
