import git
import json
from os import environ
from ..models import Osgs

osgs = Osgs.query.all()[0]
osgs_repo = json.loads(osgs.config)["osgs_repo"]

# Check out via HTTPS
# git.Repo.clone_from("https://github.com/kartoza/osgs", "/app/osgs")
git.Repo.clone_from(osgs_repo, environ["FLASK_APP_ROOT"])
# Clone via ssh (will use default keys)
git.Repo.clone_from("git@github.cim:kartoza/osgs", "/app/osgs")


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print("update(%s, %s, %s, %s)" % (op_code, cur_count, max_count, message))
        print(self._cur_line)


repo = git.Repo.clone_from(osgs_repo, "./git-python", progress=Progress())
