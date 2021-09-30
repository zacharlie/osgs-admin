import git
import json
from shutil import rmtree
from flask import current_app as app
from ..models import Osgs

osgs = Osgs.query.all()[0]
osgs_repo = json.loads(osgs.config)["osgs_repo"]

application_path = app.app_dir


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print(self._cur_line)


def get_repo(repo_path: str = osgs_repo):
    try:
        repo = git.Repo(repo_path)
        repo_issues = None
    except InvalidGitRepositoryError as e:
        repo = "Invalid Git Repository Specified"
        repo_issues = [e]
    except Exception as e:
        repo = None
        repo_issues = [e]
    finally:
        return repo, repo_issues


def get_commit_hash(repo):
    return repo.commit().hexsha


def get_remote_info(repo):
    remote = git.remote.Remote(repo, "origin")
    remote_info = remote.fetch()[0]
    remote_commit = remote_info.commit
    return remote_commit.hexsha


def get_repo_info(repo):
    heads = repo.heads
    branches = [branch for branch.name in heads]
    repo_info = {
        "commit": get_commit_hash(repo),
        "branch": repo.active_branch.name,
        "branches": branches,
    }
    return repo_info


def check_repo(repo):
    """Do Some Things"""
    pass


def clone_repo(repo_path: str = osgs_repo):
    repo = git.Repo.clone_from(repo_path, app.app_dir, progress=Progress())
    return repo


def destroy_repo(repo_path):
    try:
        rmtree(repo_path)
    except:
        raise DirectoryRemovalError
