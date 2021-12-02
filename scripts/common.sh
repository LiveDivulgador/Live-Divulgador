# project
project_name="livedivulgador"
author_name="vcwild"

# terminal color
color_default="\e[39m"
color_error="\e[31m"
color_ok="\e[32m"
color_header="\e[34m"

# paths
current_directory="$(pwd)"
virtualenv_directory="$current_directory/venv"

# functions
print_header() {
  echo
  echo -e "--$color_header $1 $color_default"
}

print_check() {
  status=$?
  if [ $status -eq 0 ]
  then
    echo -e "[$color_ok OK $color_default] $1"
  else
    echo -e "[$color_error KO $color_default] $1"
  fi
}
