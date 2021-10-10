# OSGS Admin

Administration and management console for the [Open Source GIS Stack](https://github.com/kartoza/osgs).

![Preview](https://user-images.githubusercontent.com/64078329/136703281-a87b5ec3-d60f-4b1f-ae76-9ffd9dbcc4b4.png)

## Deployment

This application is designed to run system commands against a subdirectory which holds the Open Source GIS Stack. As such, there are serious security implications regarding the exposure of this interface. The primary aim of this application is to provide a user interface for management operations which can be conveniently run on a server, and it is recommended that this infrastructure is isolated at the network level.

> **TL;DR** Do not publish this admin interface or it's host port as a public facing web application. Only access it via local network, VPN, or similarly isolated environment.

## Security

The system is designed to run docker commands from the context of the docker host machine.

It does this by mounting the hosts docker socket as `//var/run/docker.sock:/var/run/docker.sock` and then leveraging the python [docker-compose](https://pypi.org/project/docker-compose/) library into the main flask application. Whilst this is constrained to the running containers and the existing mounted volumes, it of course opens the system up to the possibility of breakouts.

In addition, the application uses the python subprocessing module to execute shell commands (within the container) for stack configuration purposes.

Over and above that, there are API endpoints for information services such as CPU and RAM utilisation of the host, which is an additional concern.

> **TL;DR** Do not publish this admin interface or it's host port as a public facing web application. Only access it via local network, VPN, or similarly isolated environment.

We'll look into locking it all down via built in wireguard or sshuttle when we get the chance.

## Platform

The admin service is a flask application designed for utilisation within a docker-compose environment. The admin interface itself is a docker-compose stack designed to manage a docker-compose stack. It relies on celery tasks with a redis backend for asynchronous activity.

## Database

The database is a simple sqlite database. If the database is not found the system will generate a new one for you if you ask nicely.

## ACL

At this time only "all or nothing" credentials are supplied. User roles have limited utility for this application, and because system calls are made directly it makes little sense to segregate permissions as privilege escalation vulnerabilities would be expected.

## Credentials

Password and username management and constraints such as complexity requirements are not currently enforced. Managing the application security is left up to the sysadmin.
