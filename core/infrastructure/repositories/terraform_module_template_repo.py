import json
import os

from core.domain.entities.exception import TemplateNotFoundException, TemplateAlreadyExistException
from core.domain.entities.terraform_module_template import TerraformModuleTemplateEntity
from core.domain.repositories.terraform_module_template_repo import BaseTerraformModuleTemplateRepository
from core.domain.repositories.git_repo import BaseGitRepository


class GitTerraformModuleTemplateRepository(BaseTerraformModuleTemplateRepository):

    def __init__(self, git_repository: BaseGitRepository, templates_path, *args, **kwargs):
        super(GitTerraformModuleTemplateRepository, self).__init__(*args, **kwargs)
        self.git = git_repository
        self.templates_path = os.path.join(self.git.local_repo_path, templates_path)
        self.templates_vars_path = os.path.join(self.git.local_repo_path, templates_path)

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

    def create(self, terraform_template_entity):
        with self.git:
            template_path = os.path.join(self.templates_path, f'{terraform_template_entity.name}.jinja2')
            template_vars_path = os.path.join(self.templates_vars_path, f'{terraform_template_entity.name}.json')
            if os.path.exists(template_path):
                raise TemplateAlreadyExistException(terraform_template_entity.name)
            with open(template_path, 'w') as f:
                f.write(terraform_template_entity.template)
            self.git.add(template_path)
            self.git.commit(f'add {template_path} to the git')
            with open(template_vars_path, 'w') as f:
                f.write(json.dumps(terraform_template_entity.variables))
            self.git.add(template_vars_path)
            self.git.commit(f'add {template_vars_path} to the git')
            self.git.push()
        return self.get(terraform_template_entity.name)

    def update(self, terraform_template_entity):
        with self.git:
            template_path = os.path.join(self.templates_path, f'{terraform_template_entity.name}.jinja2')
            template_vars_path = os.path.join(self.templates_vars_path, f'{terraform_template_entity.name}.json')
            if not os.path.exists(template_path):
                raise TemplateNotFoundException(terraform_template_entity.name)
            with open(template_path, 'w') as f:
                f.write(terraform_template_entity.template)
                self.git.add(f)
                self.git.commit(f'add {f}.json to the git')
            with open(template_vars_path, 'w') as f:
                f.write(json.dumps(terraform_template_entity.variables))
                self.git.add(f)
                self.git.commit(f'add {f}.json to the git')
            self.git.push()
        return self.get(terraform_template_entity.name)

    def delete(self, name):
        pass


class DatabaseTerraformModuleTemplateRepository(BaseTerraformModuleTemplateRepository):
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


class StorageTerraformModuleTemplateRepository(BaseTerraformModuleTemplateRepository):

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
            variables = self.__get_variables__(name)
            return TerraformModuleTemplateEntity().load({
                'name': name,
                'template': template,
                'variables': variables
            })

    def create(self, terraform_template_entity):
        template_path = os.path.join(self.templates_path, f'{terraform_template_entity.name}.jinja2')
        template_vars_path = os.path.join(self.templates_vars_path, f'{terraform_template_entity.name}.json')
        if os.path.exists(template_path):
            raise TemplateAlreadyExistException(terraform_template_entity.name)
        with open(template_path, 'w') as f:
            f.write(terraform_template_entity.template)
        with open(template_vars_path, 'w') as f:
            f.write(json.dumps(terraform_template_entity.variables))
        return self.get(terraform_template_entity.name)

    def update(self, terraform_template_entity):
        template_path = os.path.join(self.templates_path, f'{terraform_template_entity.name}.jinja2')
        template_vars_path = os.path.join(self.templates_vars_path, f'{terraform_template_entity.name}.json')
        if not os.path.exists(template_path):
            raise TemplateNotFoundException(terraform_template_entity.name)
        with open(template_path, 'w') as f:
            f.write(terraform_template_entity.template)
        with open(template_vars_path, 'w') as f:
            f.write(json.dumps(terraform_template_entity.variables))
        return self.get(terraform_template_entity.name)

    def delete(self, name):
        os.remove(os.path.join(self.templates_path, f'{name}.jinja2'))
        return f"{name} has been deleted"

    def __get_variables__(self, name):
        templates = os.listdir(self.templates_vars_path)
        if name not in [template.split('.')[0] for template in templates]:
            return {}
        else:
            vars_file_path = os.path.join(self.templates_vars_path, f'{name}.json')
            return json.loads(LocalTerraformModuleTemplateRepository.read_file(vars_file_path))

    @staticmethod
    def read_file(path):
        with open(path) as f:
            return f.read()
