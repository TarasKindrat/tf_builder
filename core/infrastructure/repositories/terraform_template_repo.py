import json
import os
from contextlib import contextmanager

from core.domain.entities.exception import (
    TemplateNotFoundException, TemplateAlreadyExistException)
from core.domain.entities.terraform_template import (
    TerraformModuleTemplateEntity)
from core.domain.repositories.terraform_module_template_repo import (
    BaseTerraformTemplateRepository)
from core.domain.repositories.git_repo import BaseGitRepository


class LocalTerraformTemplateRepository(BaseTerraformTemplateRepository):

    def __init__(self, *args, **kwargs):
        super(LocalTerraformTemplateRepository, self).__init__(*args, **kwargs)
        self.templates_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), os.path.pardir,
            os.path.pardir, 'static/templates')
        self.templates_vars_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), os.path.pardir,
            os.path.pardir, 'static/templates_vars')

    def list(self):
        templates = os.listdir(self.templates_path)
        return [template.split('.')[0] for template in templates]

    def get(self, name):
        if name not in self.list():
            raise TemplateNotFoundException()
        else:
            file_path = os.path.join(self.templates_path, f'{name}.jinja2')
            template = LocalTerraformTemplateRepository.read_file(file_path)
            variables = self.__get_variables__(name)
            return TerraformModuleTemplateEntity().load({
                'name': name,
                'template': template,
                'variables': variables
            })

    def create(self, terraform_template_entity):
        name = terraform_template_entity.name
        template_path = os.path.join(self.templates_path, f'{name}.jinja2')
        vars_path = os.path.join(self.templates_vars_path, f'{name}.json')
        if os.path.exists(template_path):
            raise TemplateAlreadyExistException(terraform_template_entity.name)
        self.__write_file(template_path, terraform_template_entity.template)
        if terraform_template_entity.variables:
            self.__write_file(vars_path, terraform_template_entity.variables)
        return self.get(terraform_template_entity.name)

    def update(self, terraform_template_entity):
        name = terraform_template_entity.name
        template_path = os.path.join(self.templates_path, f'{name}.jinja2')
        vars_path = os.path.join(self.templates_vars_path, f'{name}.json')
        if not os.path.exists(template_path):
            raise TemplateNotFoundException(terraform_template_entity.name)
        self.__write_file(template_path, terraform_template_entity.template)
        if terraform_template_entity.variables:
            self.__write_file(vars_path, terraform_template_entity.variables)
        return self.get(terraform_template_entity.name)

    def delete(self, name):
        if os.path.exists(os.path.join(self.templates_path, f'{name}.jinja2')):
            os.remove(os.path.join(self.templates_path, f'{name}.jinja2'))
            return f"{name} has been deleted"
        else:
            raise TemplateNotFoundException(name)

    def __get_variables__(self, name):
        templates = os.listdir(self.templates_vars_path)
        if name not in [template.split('.')[0] for template in templates]:
            return {}
        else:
            vars_file_path = os.path.join(
                self.templates_vars_path, f'{name}.json')
            return json.loads(LocalTerraformTemplateRepository.read_file(
                vars_file_path))

    def __write_file(self, path, content):
        content = (json.dumps(content)
                   if isinstance(content, (dict, list))
                   else str(content))
        with open(path, 'w') as f:
            f.write(content)

    @staticmethod
    def read_file(path):
        with open(path) as f:
            return f.read()


class GitTerraformTemplateRepository(LocalTerraformTemplateRepository):

    def __init__(self, git_repository: BaseGitRepository, templates_path, *args,
                 **kwargs):
        super(GitTerraformTemplateRepository, self).__init__(*args, **kwargs)
        self.git = git_repository
        self.templates_path = os.path.join(
            self.git.local_repo_path, templates_path, 'templates')
        self.templates_vars_path = os.path.join(
            self.git.local_repo_path, templates_path, 'templates_vars')

    def list(self):
        with self.git:
            return super(GitTerraformTemplateRepository, self).list()

    def get(self, name):
        with self.git:
            return super(GitTerraformTemplateRepository, self).get(name)

    def create(self, terraform_template_entity):
        with self.git_commited(terraform_template_entity.name):
            return super(GitTerraformTemplateRepository, self).create(
                terraform_template_entity)

    def update(self, terraform_template_entity):
        with self.git_commited(terraform_template_entity.name):
            return super(GitTerraformTemplateRepository, self).update(
                terraform_template_entity)

    def delete(self, name):
        with self.git:
            template_path = os.path.join(self.templates_path, f'{name}.jinja2')
            template_vars_path = os.path.join(self.templates_vars_path,
                                              f'{name}.json')
            if not os.path.exists(template_path):
                raise TemplateNotFoundException(name)
            self.__delete_git_file(template_path)
            self.__delete_git_file(template_vars_path)
            return f"{name} has been deleted"

    @contextmanager
    def git_commited(self, name):
        template_path = os.path.join(self.templates_path, f'{name}.jinja2')
        vars_path = os.path.join(self.templates_vars_path, f'{name}.json')
        yield
        # self.git.add(template_path)
        # self.git.add(vars_path)
        # self.git.commit(f'add {name} to the git')
        # self.git.push()

    def __delete_git_file(self, path):
        self.git.rm(path)
        self.git.commit(f'remove {path} from the git')
        self.git.push()


class DatabaseTerraformTemplateRepository(BaseTerraformTemplateRepository):
    def list(self):
        pass

    def get(self, name):
        pass

    def create(self, terraform_template_entity):
        pass

    def update(self, terraform_template_entity):
        pass

    def delete(self, name):
        pass


class StorageTerraformTemplateRepository(BaseTerraformTemplateRepository):

    def list(self):
        pass

    def get(self, name):
        pass

    def create(self, terraform_template_entity):
        pass

    def update(self, terraform_template_entity):
        pass

    def delete(self, name):
        pass
