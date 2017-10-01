#!/bin/bash

# Uninstall current version
pip uninstall builder -y

# Check out latest version
git checkout -- .
git pull

# Install latest version
cd builder
pip install .
cd ..
