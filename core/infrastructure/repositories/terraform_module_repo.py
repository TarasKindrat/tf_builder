from jinja2 import Environment, BaseLoader
from marshmallow import fields

from core.domain.entities.base import BaseEntity
from core.domain.entities.terraform_module import TerraformModuleEntity
from core.domain.repositories.terraform_module_repo import BaseTerraformModuleRepository


class LocalTerraformModuleRepository(BaseTerraformModuleRepository):
    def get(self, name, variables):
        pass

    def create(self, modules, terraform_template_service):
        result = []
        for module in modules:
            tf_module = TerraformModuleEntity().load(module)
            template = terraform_template_service.get(tf_module.name)
            jinja_tpl = Environment(loader=BaseLoader).from_string(template.get('template'))
            result.append(jinja_tpl.render(tf_module.variables))
        return '\n\n'.join(result)

    def update(self, name, content):
        pass

    def delete(self, name):
        pass
