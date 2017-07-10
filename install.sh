#!/bin/bash

# Uninstall package (if present)
pip uninstall builder -y

# Install package
cd builder
pip install .
cd ..
