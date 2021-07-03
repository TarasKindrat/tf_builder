
from jinja2 import BaseLoader, Environment
from marshmallow import fields

from core.application.services.base import BaseService
from core.application.services.terraform_template_service import TerraformTemplateService
from core.domain.entities.base import BaseEntity
from core.domain.entities.terraform_module import TerraformModuleEntity
from core.domain.repositories.terraform_module_repo import BaseTerraformModuleRepository


class TerraformModuleService(BaseService):
    def __init__(self, repo: BaseTerraformModuleRepository,
                 terraform_template_service: TerraformTemplateService):
        self.repo = repo
        self.terraform_template_service = terraform_template_service

    def get(self, modules):
        pass

    def create(self, modules):
        return self.repo.create(modules, self.terraform_template_service)

    def delete(self, name):
        pass

    def update(self, name, template, variables):
        pass
