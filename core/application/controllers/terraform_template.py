from core.application.controllers import BaseController
from core.application.services.terraform_template_service import \
    TerraformTemplateService


class TerraformTemplate(BaseController):
    def __init__(self, service: TerraformTemplateService):
        self.service = service

    def list(self):
        return {"modules": self.service.list()}

    def get(self, name):
        return self.service.get(name)

    def create(self, params):
        name = params.get("name")
        template = params.get("template", params.get("template_file"))
        return self.service.create(name, template)

    def update(self, name, params):
        template = params.get("template", params.get("template_file"))
        return self.service.update(name, template)

    def delete(self, name):
        return self.service.delete(name)

