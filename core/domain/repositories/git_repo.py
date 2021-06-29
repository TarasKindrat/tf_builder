class BaseGitRepository(object):
    def __init__(self, local_repo_path, user_name, password):
        self.git = None
        self.local_repo_path = local_repo_path
        self.user_name = user_name
        self.password = password

    def __enter__(self):
        self.pull()
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __clone__(self, repo_url, repo_path, user_name, password):
        raise NotImplementedError

    def pull(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError

    def push(self):
        raise NotImplementedError

    def branch(self):
        raise NotImplementedError

    def checkout(self):
        raise NotImplementedError
