#!/usr/bin/zsh
# To test detect-wsl on different python versions using pyenv
# Should work using bash too, just change the shebang

# This script must be run in the project base directory (the one containing README.md etc.)
# Before running it, put the expected output in the `test/reference_output.out` file
# (the expected output will depend on your OS and environment - see README.md for an example)

mkdir -p test

# pyenv init
PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

declare -a myPyVersions
myPyVersions=("3.5" "3.6" "3.7" "3.8" "3.9" "3.10" "3.11" "3.12" "3.13")

# Make sure we have all these versions installed
pyenv install --skip-existing ${myPyVersions[@]}
# If this script was interrupted, test_env might still exist and could be broken
# So just remove it
pyenv virtualenv-delete -f test_env

for pyVersion in "${myPyVersions[@]}"; do
  echo Testing on ${pyVersion}
  outputFile="test/test_output_${pyVersion}.out"
  # Clear the output file to make sure we fail the test in case of an error
  echo "" > ${outputFile}
  pyenv virtualenv $pyVersion test_env > /dev/null
  pyenv activate test_env
  python -m pip install --upgrade pip wheel setuptools > /dev/null
  python -m pip install -e . > /dev/null
  python -m detect_wsl > ${outputFile}
  pyenv deactivate
  pyenv virtualenv-delete -f test_env
  if cmp -s ${outputFile} test/reference_output.out; then
    echo Passed on Python ${pyVersion}!
  else
    echo Failed on Python ${pyVersion}
  fi
done
