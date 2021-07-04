import dataclasses

import jinja2schema

from core.application.services.base import BaseService
from core.domain.entities.terraform_template import TerraformTemplateEntity
from core.domain.repositories.terraform_template_repo import (
    BaseTerraformTemplateRepository)


class TerraformTemplateService(BaseService):
    def __init__(self, repo: BaseTerraformTemplateRepository):
        self.repo = repo

    def list(self):
        return sorted(self.repo.list())

    def get(self, name):
        template = dataclasses.asdict(self.repo.get(name))
        variables = jinja2schema.infer(template.get('template'))
        template['variables'] = jinja2schema.to_json_schema(variables)
        return template

    def create(self, name, template):
        terraform_template_entity = TerraformTemplateEntity().load({
            "name": name,
            "template": template
        })
        return dataclasses.asdict(self.repo.create(terraform_template_entity))

    def delete(self, name):
        return self.repo.delete(name)

    def update(self, name, template):
        terraform_template_entity = TerraformTemplateEntity().load({
            "name": name,
            "template": template
        })
        return dataclasses.asdict(self.repo.update(terraform_template_entity))
