# Docker integration

This package contains some sample docker integrations.

## Actions

### Build docker image

This action builds a docker image given a path to Dockerfile (could be
directory containing Dockerfile or path to Dockerfile or remote URL containing
Dockerfile) and a tag to use for the image.

### Pull docker image

This action pulls a docker image from docker registry. Image is identified by repository and tag.

### Push docker image

This action pushes an image to a docker registry. Image is identified by repository and tag.

## Sensors

### Docker container spun up/shut down

This sensor watches the list of containers on local box and sends triggers
whenever a new container is spun up or an exisiting one is shut down.

This sensor exposes the following triggers:

* `docker.container_tracker.started` - Dispatched when a new container has
  been detected / started
* `docker.container_tracker.stopped` - Dispatched when an existing container
  has been stopped

## Requirements

1. Python 2.7 or greater
2. docker-io (version 1.13 or later)
3. pip install docker-py (0.4.0 or later)

YMMV if you use versions not listed here.

## Configuration

1. Edit config.yaml and look at the options. These options mirror the options
   of docker CLI.

## Notes

If you are connecting to the Docker daemon via the Unix socket, you need to
make sure that this socket is accessible to the system user under which
StackStorm processes are running.

For example, if `stanley` is the name of the system user, he should be added to `docker` group like so:

* sudo usermod -a -G docker stanley
* sudo service docker restart

(If you are currently logged on as the user you are trying to add, you will have to logout/log back in.)
