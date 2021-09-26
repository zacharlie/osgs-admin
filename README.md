# OSGS Admin

Administration and management console for the [Open Source GIS Stack](https://github.com/kartoza/osgs).

## Deployment

This application is designed to run system commands against a subdirectory which holds the Open Source GIS Stack. As such, there are serious security implications regarding the exposure of this interface. The primary aim of this application is to provide a user interface for management operations which can be conveniently run on a server, and it is recommended that this infrastructure is isolated at the network level.

> **TL;DR** Do not publish this interface as a public facing web application. Only access it via local network, VPN, or similarly isolated environment.

## Security

The system is designed to run docker commands from the context of the docker host machine. API will be great buuuuut we might just use [the most pointless command ever](https://zwischenzugs.com/2015/06/24/the-most-pointless-docker-command-ever/). Time will tell.

Honestly this seems like a bad idea:

```
docker run -ti
    --privileged
    --net=host --pid=host --ipc=host
    --volume /:/host
    busybox
    chroot /host
```

## Platform

The admin service is a flask application designed for utilisation within a docker-compose environment. The admin interface itself is a docker-compose stack designed to manage a docker-compose stack. It relies on celery tasks with a redis backend for asynchronous activity.

## Database

The database is a simple sqlite database. If the database is not found the system will generate a new one for you if you ask nicely.

## ACL

At this time only "all or nothing" credentials are supplied. User roles have limited utility for this application, and because system calls are made directly it makes little sense to segregate permissions as privilege escalation vulnerabilities would be expected.

## Credentials

Password and username management and constraints such as complexity requirements are not currently enforced. Managing the application security is left up to the sysadmin.
