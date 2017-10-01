#!/bin/bash

# Uninstall package (if present)
sudo pip uninstall gesso -y

# Install package
cd gesso 
sudo pip install .
cd ..
