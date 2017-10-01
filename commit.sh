#!/bin/bash

message="Update."
if [ ! $# -eq 0 ]; then
	message="$1"
else
	message="Update."
fi;

git add .
git commit -m "$message"
git push
