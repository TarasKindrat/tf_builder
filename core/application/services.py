import jinja2schema

from core.domain.repositories.terraform_module_template_repo import BaseTerraformModuleTemplateRepository


class BaseService(object):
    pass


class TerraformModuleService(BaseService):
    def __init__(self, repo: BaseTerraformModuleTemplateRepository):
        self.repo = repo

    def list(self):
        return sorted(self.repo.list())

    def get(self, name):
        template = self.repo.get(name)
        variables = {}
        jinja_variables = vars(jinja2schema.infer(template))
        if jinja_variables.get('data'):
            variables = self.repo.get_variables(name)
        return {
            "name": name,
            "template": template,
            "variables": variables,
        }

    def create(self, name, content):
        return self.repo.create(name, content)

    def delete(self, name):
        return self.repo.delete(name)

    def update(self, name, content):
        return self.repo.update(name, content)
