#!/bin/bash

# Uninstall current version
pip uninstall gesso -y

# Check out latest version
git checkout -- .
git pull

# Install latest version
cd gesso
pip install .
cd ..
