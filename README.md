# OSGS Admin

Administration and management console for the [Open Source GIS Stack](https://github.com/kartoza/osgs).

## Deployment

This application is designed to run system commands against a subdirectory which holds the Open Source GIS Stack. As such, there are serious security implications regarding the exposure of this interface. The primary aim of this application is to provide a user interface for management operations which can be conveniently run on a server, and it is recommended that this infrastructure is isolated at the network level.

> **TL;DR** Do not publish this interface as a public facing web application. Only access it via local network, VPN, or similar

## Database

The database is a simple sqlite database. If the database is not found the system will generate a new one.

## Application Security

At this time only "all or nothing" credentials are supplied. User roles have limited utility for this application, and because system calls are made directly it makes little sense to segregate permissions and privilege escalation vulnerabilities could be expected.

## Passwords

The application bootstraps a database with the default username and password `admin`. Although it is highly recommended that this be changed immediately, such behaviours are not enforced. In addition, there is no constraint on the password complexity. Managing the application security is left up to the sysadmin.

