#!/bin/bash
pip uninstall builder -y & pip install . & git add * & git commit -m "Updated library." & git push
