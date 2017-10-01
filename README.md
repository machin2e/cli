# Gesso 

[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/machineee/home)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Thank you for checking out Gesso. We're changing Gesso every day as we crank out the [roadmap]() and make tweaks along the way. If you want to help out, learn how to do so in the [contribution](#contribute) section. Thanks for bearing with us :bear:!

This repository contains:

1. Gesso command line environment (CLE) 
2. Gesso Python API

## Installation

Install with the following command. You may want to prefix the command with `sudo`.

```
pip install git+https://github.com/machineeeee/gesso
```

## Getting Started

### Create a Project

#### Create a Project Workspace

To create a project, navigate to the folder into which you'd like `gesso` to create a project folder, in which all project content will be stored. Then run this command:

```
gesso new my-system-project
```

This command generates a new project directory. You can read about that in the [Project Layout and Data Format](#projects-and-files) section.

#### Add Components to Project

TODO

#### Assemble Components (into Systems)

TODO

#### Script the Controllers

TODO

### Distribute a Project

#### Generate Assembly Instructions

TODO

## Usage

Gesso is a command line application. It can be used by running commands like this one:

```
gesso connect --model raspberry-pi-3 --model machineee/generic-servo --model ir-rangefinder --model ir-rangefinder
```

### `gesso new`

_Examples:_
```
gesso new Used to initialize this folder (assigns a default name).
gesso new -v					Used to create and init a VM (via Vagrant).
gesso new fiery-fox -v			Used to initialize a new VM named fiery-fox.
gesso new desktop				Used to init a Gesso env called desktop.
```

### `gesso start`
### `gesso stop`
### `gesso announce`
### `gesso manage`

### `gesso device`
#### `gesso device list|add|remove`

### `gesso interface`
### `gesso view`

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

## Projects and Files

### Project Directory Structure

Once you create a new project with the `gesso init` command, you'll have a project directory with a well-definned structure, shown below:

```
my-system-project
├── README.md (optional)
├── .gesso
│   ├── config
│   ├── logs
│   ├── components
│   ├── hosts/devices
│   └── hosts
├── project.yaml/package.yaml
├── .gitignore
├── interfaces/modules
│   └── TODO: resolve this folder with the servo, steering-mechanism, etc. interfaces. Make a regular format.
├── servo
│   ├── interface.yaml/component.yaml
│   └── controller.py
├── steering-mechanism
│   ├── interface.yaml
│	├── controller.py
│   ├── left-servo
│   │   ├── interface.yaml
│   │   └── controller.py
│   └── right-servo
│       ├── interface.yaml
│       └── controller.py
├── src? 
│   ├── favicon.ico
│   ├── index.html
│   └── manifest.json
└── docs?
    ├── App.css
    ├── App.js
    ├── App.test.js
    ├── index.css
    ├── index.js
    ├── logo.svg
    └── registerServiceWorker.js
```

The `.gitignore` file ignores the `.gesso` folder, which will be regenerated uniquely on each host machine.

### Device Configuration File

```
name: Human-readable Device Name
description: Any desription!
host:
	strategy: developer
```

To configure a host as a platform host, start with the following file:

```
name: Human-readable Device Name
description: Any desription!
host:
	strategy: platform
```

To exclude the device from the system, don't create a host interface for the device. Simply omit the `host` component from the `config` file.

### Component Model File Format

Component (or device) model files need to be formatted in [[YAML]] markup. These files have the `*.yaml` extension.

An example device model file is given below (this is the same as <path>):

```
YAML device file here...
```
### System/Path Model File Format

TODO

## Command Line Interface

### Usage

```
gesso connect --model raspberry-pi-3 --model machineee/generic-servo --model ir-rangefinder --model ir-rangefinder
```

#### `gesso new`

This command is used to generate a project directory to serve as a _workspace_ for a project. The workspace file system generated is a file hierarchy defined by the structure of described in [Projects and Files](#projects-and-files).

The `gesso new` command is typically run from a device that will be used to develop systems with Gesso. Devices only used by developers are called _developer hosts_. Devices can also be included in systems associated with a projects. Such hosts are called _platform hosts_. To include developer and platform hosts in a system configuration, edit the `.gesso/config` YAML file. Change the _host strategy_ setting to `developer` or `platform` as desired for your project.

Note that one use case for project configurations is to establish _developer configuration_ and a _deployment configuration_. However, we have strong opinions on the long-term viability of supporting multiple configurations since we wish to dissolve barriers between developers and non-developers. As a result, we suggest experimenting with designing and deploying systems so your project doesnt' havem lultiple configurations. We may altogether omit support for multiple configurations in the future. If you have strong feelings about this matter, please express them on Gitter or create an issue.

_Examples:_
```
gesso new					Used to initialize this folder (assigns a default name).
gesso new -v					Used to create and init a VM (via Vagrant).
gesso new fiery-fox -v			Used to initialize a new VM named fiery-fox.
gesso new desktop				Used to init a Gesso env called desktop.
```

#### `gesso start`

Starts the `gessod` platform service, exposing the host device as part of the Gesso platform in a project workspace. Upon execution, Gesso will load the configuration in the file `.gesso/config` (see more about it [here](#device-config-file). Once a host has been exposed to the Gesso platform with a host interface, the host's services, such as I/O pins, will be exposed as specialized interfaces composed within the host interface (which is the top-level interface for the device). These interfaces are pre-processed by the Gesso APIs, enabling the APIs to use higher-than-usual level of hardware abstraction with relatively little performance cost. The interfaces further determine what will be made available to the Gesso APIs on the device and, optionally, exposed to other devices in the network.

Once run on a device, Gesso will automatically discover other platform hosts, record them in a database index, and continue to monitor their status. If configured as a `platform` host, the device will also be exposed for other hosts to discover and use.

#### `gesso stop`

Stops the `gesso` service (if running) on a host.

#### `gesso manage`

#### `gesso component`

Previously `gesso device`. May revert. Still sorting out the terminology that will be used throughout the platform architecture.

##### `gesso component list|add|remove`

Previously `gesso device`. May revert. Still sorting out the terminology that will be used throughout the platform architecture.

#### `gesso interface`

#### `gesso view`

#### `gesso signup`

Assists you in creating an account for accessing the Machineee platform. You must use your GitHub account.

#### `gesso login`

Logs you in with Machineee account credentials. If run from a project workspace, only the project will be associated with the account.

**Proposed Commands**

```
help
note [add|remove|list]		Used to add, remove, or list notes for a device or environment/workspace/project.
assemble			Starts interactive self-assembly.
start [broadcast|discover]
status [broadcast|discover]
run [broadcast|discover]
stop [broadcast|discover]
monitor [broadcast|discover]

log
gesso announce: Starts broadcasting the device on the network, making it discoverable by other Gesso hosts on the network.
```

## API

This repository contains the Python API for using hardware resources, mesh and Internet network services and resources, and the Machineee servers.

The API will include interfaces for:
- Port and protocol physical I/O.
- Higher-level interfaces defined for devices that expose device-specific functionality through abstraction of port and protocol-level interfaces.
- Internet and mesh communications protocols (HTTP, HTTPS, GraphQL, Thread, pub-sub).
- Device state (power level, peripheral and I/O connectedness states)
- Host state (subscribers, available services)
- Network state (peers, subscriptions)
- System status

## Contribute

If you want to contribute, you might find GitHub's [Open Source Guides](https://opensource.guide/) useful. For example, there's a guide on [code of conduct](https://opensource.guide/code-of-conduct/) for open source projects. The repository for the guides is at ([GitHub](https://github.com/github/opensource.guide#readme)). You can find more about [the anatomy of an open source project](https://opensource.guide/how-to-contribute/#anatomy-of-an-open-source-project) and GitHub's [community profiles](https://help.github.com/articles/viewing-your-community-profile/), too.
