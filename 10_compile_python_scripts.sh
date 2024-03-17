#!/bin/bash

# compileall uses only one core
# 100k scripts take around 2-3 minutes
# for some scripts the compilation fails, this is expected (different versions of python)
python -m compileall -qq -j 4 -d . ../data/codeparrot-clean-train/original_code
version=$(python --version | cut -c 8-)
mkdir -p ../data/codeparrot-clean-train/compiled-$version/
# mv does not work with 100k files:
# mv ../data/codeparrot-clean-train/original_code/__pycache__/* ../data/codeparrot-clean-train/compiled-$version/
echo ../data/codeparrot-clean-train/original_code/__pycache__/*.pyc | xargs mv -t ../data/codeparrot-clean-train/compiled-$version/ --