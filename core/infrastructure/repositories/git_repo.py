from git import Repo
import os

from core.domain.repositories.git_repo import BaseGitRepository


class GitRepository(BaseGitRepository):

    def __init__(self, repo_path, user_name, password, repo_url=None):
        super(GitRepository, self).__init__(repo_path, user_name, password)
        self.git = self.__clone__(repo_url, repo_path, user_name, password) \
            if not os.path.exists(repo_path) and repo_url else self.__init_repo__(repo_path)

    @staticmethod
    def __clone__(repo_url, repo_path, user_name, password):
        return Repo.clone_from(repo_url, repo_path)

    @staticmethod
    def __init_repo__(repo_path):
        return Repo(repo_path)

    def pull(self):
        o = self.git.remotes.origin
        o.pull()

    def commit(self):
        pass

    def push(self):
        pass

    def branch(self):
        pass

    def checkout(self):
        pass