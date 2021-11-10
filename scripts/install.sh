#!/bin/bash

source $(dirname "$0")/common.sh

current_directory="$(pwd)"
virtualenv_directory="$current_directory/venv"

main() {
  print_header "Preparing python virtual environment"

  python3 -m venv "$virtualenv_directory" >/dev/null 2>&1
  print_check "virtualenv initialization $virtualenv_directory"

  $virtualenv_directory/bin/pip install --upgrade pip >/dev/null 2>&1
  print_check "pip upgrade"

  $virtualenv_directory/bin/pip install setuptools_scm >/dev/null 2>&1
  print_check "pip install setuptools_scm"

  # install local development build
  echo -e "       ... installing Livedivulgator bot component"
  $virtualenv_directory/bin/pip install -e .[dev] >/dev/null 2>&1
  print_check "bot installation"

  # check installation
  echo -e "       ... checking CLI"
  $virtualenv_directory/bin/divulgator --help >/dev/null 2>&1
  print_check "divulgator CLI installation"
}

# main
main
