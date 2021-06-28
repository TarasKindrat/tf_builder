
from jinja2 import BaseLoader, Environment
from marshmallow import fields

from core.application.services.base import BaseService
from core.application.services.terraform_module_template_service import TerraformModuleTemplateService
from core.domain.entities.base import BaseEntity
from core.domain.entities.terraform_module import TerraformModuleEntity
from core.domain.repositories.terraform_module_repo import BaseTerraformModuleRepository


class TerraformModuleService(BaseService):
    def __init__(self, repo: BaseTerraformModuleRepository,
                 terraform_template_service: TerraformModuleTemplateService):
        self.repo = repo
        self.terraform_template_service = terraform_template_service

    def get(self, modules):
        pass

    def create(self, modules):
        result = []
        for module in modules:
            tf_module = TerraformModuleEntity().load(module)
            template = self.terraform_template_service.get(tf_module.name)
            mapping = {
                "str": fields.String,
                "string": fields.String,
                "bool": fields.Boolean,
                "int": fields.Integer
            }
            variables = {k: mapping.get(v.get('type'))(required=v.get('required'))
                         for k, v in template.get('variables').items()}
            clz = type("TemplateVariables", (BaseEntity,), variables)
            clz().load(tf_module.variables)
            jinja_tpl = Environment(loader=BaseLoader).from_string(template.get('template'))
            result.append(jinja_tpl.render(tf_module.variables))
        return '\n\n'.join(result)

    def delete(self, name):
        pass

    def update(self, name, template, variables):
        pass
