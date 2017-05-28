#!/bin/bash

for argument in "$@"
do
	echo "$argument"
	if [ "$argument" = "git" ]; then
		echo "GIT"
	fi;
done

pip uninstall builder -y
cd builder
pip install .
cd ..

git add *
git commit -m "Updated library."
git push
