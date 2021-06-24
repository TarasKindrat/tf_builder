import json
import os
from abc import abstractmethod

from core.domain.entities.exception import TemplateNotFoundException
from core.domain.repositories.terraform_module_template_repo import BaseTerraformModuleTemplateRepository
from core.domain.repositories.git_repo import BaseGitRepository


class GitTerraformModuleTemplateRepository(BaseTerraformModuleTemplateRepository):

    def __init__(self, git_repository: BaseGitRepository, templates_path, *args, **kwargs):
        super(GitTerraformModuleTemplateRepository, self).__init__(*args, **kwargs)
        self.git = git_repository
        self.templates_path = os.path.join(self.git.local_repo_path, templates_path)

    def list(self):
        with self.git:
            templates = os.listdir(self.templates_path)
            return [template.split('.')[0] for template in templates]

    def get(self, name):
        with self.git:
            if name not in self.list():
                raise TemplateNotFoundException()
            else:
                file_path = os.path.join(self.templates_path, f'{name}.jinja2')
                with open(file_path) as f:
                    return f.read()

    def get_variables(self, name):
        pass

    def create(self, name, content):
        pass

    def update(self, name, content):
        pass

    def delete(self, name):
        pass


class DatabaseTerraformModuleTemplateRepository(BaseTerraformModuleTemplateRepository):
    def get_variables(self, name):
        pass

    def list(self):
        pass

    def get(self, name):
        pass

    def create(self, name, content):
        pass

    def update(self, name, content):
        pass

    def delete(self, name):
        pass


class StorageTerraformModuleTemplateRepository(BaseTerraformModuleTemplateRepository):
    def get_variables(self, name):
        pass

    def list(self):
        pass

    def get(self, name):
        pass

    def create(self, name, content):
        pass

    def update(self, name, content):
        pass

    def delete(self, name):
        pass


class LocalTerraformModuleTemplateRepository(BaseTerraformModuleTemplateRepository):

    def __init__(self, *args, **kwargs):
        super(LocalTerraformModuleTemplateRepository, self).__init__(*args, **kwargs)
        self.templates_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir,
                                           'static/templates')
        self.templates_vars_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir,
                                                os.path.pardir, 'static/templates_vars')

    def list(self):
        templates = os.listdir(self.templates_path)
        return [template.split('.')[0] for template in templates]

    def get(self, name):
        if name not in self.list():
            raise TemplateNotFoundException()
        else:
            file_path = os.path.join(self.templates_path, f'{name}.jinja2')
            template = LocalTerraformModuleTemplateRepository.read_file(file_path)
            return template

    def get_variables(self, name):
        templates = os.listdir(self.templates_path)
        if not name in [template.split('.')[0] for template in templates]:
            raise TemplateNotFoundException()
        else:
            vars_file_path = os.path.join(self.templates_vars_path, f'{name}.json')
            return json.loads(LocalTerraformModuleTemplateRepository.read_file(vars_file_path))

    def create(self, name, content):
        pass

    def update(self, name, content):
        pass

    def delete(self, name):
        pass

    @staticmethod
    def read_file(path):
        with open(path) as f:
            return f.read()
