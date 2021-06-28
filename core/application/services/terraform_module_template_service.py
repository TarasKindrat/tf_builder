import dataclasses
import json

from core.application.services.base import BaseService
from core.domain.entities.terraform_module_template import TerraformModuleTemplateEntity
from core.domain.repositories.terraform_module_template_repo import BaseTerraformModuleTemplateRepository


class TerraformModuleTemplateService(BaseService):
    def __init__(self, repo: BaseTerraformModuleTemplateRepository):
        self.repo = repo

    def list(self):
        return sorted(self.repo.list())

    def get(self, name):
        return dataclasses.asdict(self.repo.get(name))

    def create(self, name, template, variables):
        terraform_template_entity = TerraformModuleTemplateEntity().load({
            "name": name,
            "template": template,
            "variables": variables,
        })
        return dataclasses.asdict(self.repo.create(terraform_template_entity))

    def delete(self, name):
        return self.repo.delete(name)

    def update(self, name, template, variables):
        terraform_template_entity = TerraformModuleTemplateEntity().load({
            "name": name,
            "template": template,
            "variables": json.loads(variables),
        })
        return dataclasses.asdict(self.repo.update(terraform_template_entity))