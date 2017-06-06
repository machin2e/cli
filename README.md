*Warning: Everything in this repository is under active development, so it is all subject to change.*

```
▒█▀▀█ ▒█░▒█ ▀█▀ ▒█░░░ ▒█▀▀▄ ▒█▀▀▀ ▒█▀▀█ 
▒█▀▀▄ ▒█░▒█ ▒█░ ▒█░░░ ▒█░▒█ ▒█▀▀▀ ▒█▄▄▀ 
▒█▄▄█ ░▀▄▄▀ ▄█▄ ▒█▄▄█ ▒█▄▄▀ ▒█▄▄▄ ▒█░▒█ 
```

## Description

This repository contains:

1. Builder CLI
2. Builder Python API

## Command Line Interface

### Usage

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
