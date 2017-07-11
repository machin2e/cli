#!/bin/bash

# Uninstall package (if present)
sudo pip uninstall builder -y

# Install package
cd builder
sudo pip install .
cd ..
