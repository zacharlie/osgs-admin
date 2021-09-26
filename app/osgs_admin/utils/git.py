import git
import json
from flask import current_app as app
from ..models import Osgs

osgs = Osgs.query.all()[0]
osgs_repo = json.loads(osgs.config)["osgs_repo"]


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print(self._cur_line)


repo = git.Repo.clone_from(osgs_repo, app.app_dir, progress=Progress())
