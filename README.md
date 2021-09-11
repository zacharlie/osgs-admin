# Hot Flask

Simple python flask app with file watcher and hot reloading using docker compose.

## About

Running flask in a docker environment is a bit painful when it comes to handling debug modes, hot reloading, and using filewatchers. This project is probably most useful for development and gitops, especially where you plan on running your application in a docker-compose, but it wasn't designed specifically for production deployments as is. YMMV.

## Components

- Python Flask - Your application
- [UWSGI & Touch Reload](https://uwsgi-docs.readthedocs.io/en/latest/Management.html#reloading-the-server) - To reload the server every time the reloader file is touched
- [Watchdog](https://pypi.org/project/watchdog/) - To monitor the app directory for changes and touch the reloader file
- Nginx - For doing what nginx does

## Running

Just use docker-compose from the root directory.

- First run: `docker-compose up -d --build`
- Start: `docker-compose up -d`
- Stop: `docker-compose down`

Windows users should check the gotchas.

## Access

Open your browser to `http://127.0.0.1:5000/` while it's running.

## Testing

Try edit 'Hello World!' in `/app/core/__init__.py.py` and refresh your browser to watch the magic happen.

## Modifying

This config expects environment variables for source and target app directories to mount the relevant volumes correctly. The reason that approach was chosen instead of named volumes was just to simplify things when running with the defaults, but you could switch that config out in the compose config. Just be aware that the ENVs need to be defined in the containers when making those changes. If you want to change the port number remember that compose is binding host 5000 to the nginx 80, so change that parameter only and don't go poking about breaking the other config between services.

## Gotchas

This seemed a lot simpler at the outset, and a couple of strange behaviours made things blurry so I reckon it's worth pointing them out.

### WSL2 Docker File Watching

Docker for windows has some issues regarding file watchers 🎉

Basically, WSL uses a CIFS mount, which doesn't trigger the necessary events in the linux kernel to have containers be notified. The issues about it raised on the [Docker Forum](https://forums.docker.com/t/file-system-watch-does-not-work-with-mounted-volumes/12038) and [WSL GitHub](https://github.com/microsoft/WSL/issues/4739) indicate it's unlikely to go resolved for a while though.

> Just a note that I first identified it (after many hours of frustration) [from a stack overflow post](https://stackoverflow.com/questions/50010421/watchdog-observer-not-running-in-container) which pointed me to a [workaround script](http://blog.subjectify.us/miscellaneous/2017/04/24/docker-for-windows-watch-bindings.html), but alas, that doesn't work for WSL2. But kudos to the internet community members who pointed me in the right direction anyway.

There are a few solutions to this, the simplest being **storing and mounting the local volume inside the WSL subsystem** (i.e your repo is in 'ubuntu' `~/hot-flask/` and not `/mnt/x/hot-flask` and you're running docker from WSL directly). Considering that WSL stores the VM disk in AppData (and moving it is non-trivial), this is hardly the ideal situation in a world of network shares, collaboration, and high-speed-lower-capacity primary disks. Also, seeing as this project is specifically designed to resolve issues like that, seems like some effort should go into addressing this. For anybody who finds this feasible but wants to access their project with a more native windows experience, you can simply access your project from `\\wsl$\Ubuntu\home\username\dev\hot-flask` or similar using explorer and vscode.

This brings us to solution two - using filesystem polling. Again, less than ideal, but nonetheless effective considering the project is designed primarily for dev work.

The `watcher-poll.py` has a reconfigured version of the watchdog script which uses a PollingObserver. For ease of configuration, there is a preconfigured `dockerfile-watchdog-poll` build, which is also configured in `docker-compose-poll.yml`, so it should be pretty simple to switch to the relevant setup. Probably makes the repo structure a bit more confusing, but seems more reasonable than another environment variable or something.

Basically, if you're using Docker on Windows, run `docker-compose -f docker-compose-poll.yml up`

### uWSGI Callable Weirdness

The initial project structure was just `./app/app.py`, but for some reason as soon there were attempts to use more complex project structures, the flask application started malfunctioning. Apparently there was some sort of naming conflict which was described in a [Stack Overflow Post](https://stackoverflow.com/questions/56774122/uwsgi-nginx-flask-unable-to-load-app-0-mountpoint-callable-not-found-or-i/69097480#69097480), so the current structure, although maybe a bit more convoluted than the standard flask hello world, at least seems to be fairly robust (and easily extensible).

## Autorefresh

You could set up quart instead of flask for async/ ws, use long polling, or configure any other system you like for more effective client side refreshing of the browser. But that's out of scope for what this intends on achieving and you'll have to implement it yourself

## Debugging

You're on your own there...
