#!/usr/bin/sh

source $(dirname "$0")/common.sh

# Build the container

container_name="vcwild/livedivulgator:$TAG_RELEASE"

main() {
  if [[ -z "${TAG_RELEASE}" ]]; then
    TAG_RELEASE="latest"
    echo -e "Preparing container with tag:${TAG_RELEASE}"
  else
    echo -e "Preparing container with tag:${TAG_RELEASE}"
  fi

  print_header "Building the container, please wait..."
  docker build -t $container_name .
}

main
