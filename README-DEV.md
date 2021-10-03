# OSGS Admin Development

This serves as the basic developer info documentation for the OSGS Admin app (at least until there is a proper docs project instantiated).

## Design

The core concepts of the application is building a docker-compose app that is used to manage a particular docker-compose app in an intuitive and user-friendly way, especially for users with more limited development expertise.

The requirements and considerations for it's design are therefore outlined as:

- Requires connecting application containers to host resources
- Asynchronous tasks are needed to perform system calls from web application
- Due to it's nature, it is not designed to be exposed publicly over the internet

As a result, the app focusses on achieving the following design objectives:

- Minimalist design - do one thing well
- Minimise utilisation of extraneous dependencies
- Package or provide all static resources to be offline-capable

## Security

Obviously, mounting various host system resources is incredibly dangerous for a webapp. There's not much else to say about this tbh.
We can try to keep dependencies to a minimum, and use flask-login, but at the end of the day I don't think this could be considered a secure app.

## Structure

The core backend application is Nginx + Flask as a web application/ UI, with Redis + Celery as task brokers for asynchronous operations.

The core of the frontend uses bulma css, animate.css, charts.js, material icons, and alpine.js for async and reactivity.

The application structure mostly tries to make things decoupled between the front and backends, in that most of the metrics etc are delivered to a rest endpoint which is consumed by the frontend.
Mucking around with async complexity seems redundant, so we rather just poll a rest endpoint for updates instead. even if it's not super efficient it's simple.
Because the endgame is to move to a more distributed cloud based platform, most operations are expected to use rest api endpoints eventually anyway.

The operations are also mostly just post functions which call celery tasks. Where things aren't configured this way, the intention is to change them to do so.

The flask application structure is also split up into various logical components to keep things a bit neater.
Of course this means if you're extending the app you need to understand the structure for imports.

This is supposed to help:

```text
├── app                                         The application directory that is bound
│   │                                           to the stack instance at /app/ by default
│   │
│   ├── app.py                                  Flask app runner
│   │
│   ├── reloader                                Blank reloader which restarts uWSGI when touched
│   │                                           and is used by watchdog for hot reloading in dev
│   │
│   ├── osgs                                    The OSGS repo directory (default is osgs)
│   │   │
│   │   └── docker-compose.yaml                 The stack is currently based on docker-compose
│   │
│   ├── osgs_admin                              Core OSGS Admin application directory
│   │   │
│   │   ├── static                              Flasks static assets
│   │   │
│   │   ├── config                              Application configuration
│   │   │   │
│   │   │   ├── __init__.py                     Base setter and getter methods for configs
│   │   │   │
│   │   │   ├── config.json                     Default user config file
│   │   │   │
│   │   │   └── osgs_default_config.py          Default app config for database bootstrap and
│   │   │                                       reset operations - not user editable
│   │   │
│   │   ├── auth.py                             Blueprint for flask login and user operations
│   │   │
│   │   ├── main.py                             Main blueprint for public pages and dashboard
│   │   │
│   │   ├── ops.py                              Operations blueprint for osgs-admin config tasks
│   │   │
│   │   ├── db.sqlite                           Default database location
│   │   │
│   │   ├── models.py                           Flask models
│   │   │
│   │   ├── tasks                               Jobs, tasks, and related utilities for Celery
│   │   │
│   │   ├── templates                           Flask html templates
│   │   │   │                                   Template pages intended to be reused or extended
│   │   │   │                                   will have a leading underscore by convention.
│   │   │   │                                   The main pages stored within this root will be
│   │   │   │                                   core app pages such as login.html, error.html etc
│   │   │   │
│   │   │   ├── components                      Component templates and jinja macros, such as loaders,
│   │   │   │                                   progress bars, modals, toasts, and other ui/ ux elements.
│   │   │   │
│   │   │   ├── config                          Configuration and settings page templates
│   │   │   │
│   │   │   ├── dashboard                       Dashboard page templates
│   │   │   │
│   │   │   ├── ops                             Operation specific pages, designed for performing
│   │   │   │                                   functions and checking status, such as cloning
│   │   │   │                                   a git repository or resetting some configurations
│   │   │   │
│   │   │   ├── users                           User operation templates, including the users
│   │   │   │                                   data table and CRUD operations like password resets
│   │   │   │
│   │   │   └── utils                           Jinja macros, utilities, and helper functions for
│   │   │                                       use in templates, such as generic type casting or
│   │   │                                       uuid generation for DOM component ids etc
│   │   │
│   │   └── utils                               Utilities and helper functions for use within flask,
│   │                                           such as retrieving docker, git, or system stats
│   │
│   ├── tests                                   What it says on the box
│   │
│   └── uwsgi.ini                               The uwsgi app config. Note that this is for the
│                                               admin app itself and not the stack, so threading
│                                               etc is not going to affect the OSGS stack performance
│
└── docker-compose.yml                          Get going with just `docker-compose up -d`
```
