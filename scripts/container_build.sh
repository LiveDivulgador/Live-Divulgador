#!/usr/bin/sh

source $(dirname "$0")/common.sh

# Build the container

main() {
  if [[ -z "${TAG_RELEASE}" ]]; then
    TAG_RELEASE="latest"
    echo -e "Preparing container with tag:${TAG_RELEASE}"
  else
    echo -e "Preparing container with tag:${TAG_RELEASE}"
  fi

  core_container_name="$author_name/$project_name"
  container_app_name="${core_container_name}_app:$TAG_RELEASE"

  container_db_name="${core_container_name}_db:$TAG_RELEASE"

  print_header "Preparing $project_name container builds"

  echo -e "       ... building $project_name app component"
  docker build -t $container_app_name -f ./docker/app.Dockerfile . > /dev/null 2>&1
  print_check "divulgador app container build"

  echo -e "       ... building $project_name database component"
  docker build -t $container_db_name -f ./docker/database.Dockerfile ./docker > /dev/null 2>&1
  print_check "divulgador database container build"
}

main
