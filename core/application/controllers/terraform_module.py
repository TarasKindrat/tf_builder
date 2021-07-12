from core.application.controllers import BaseController
from core.application.services.terraform_module_service import TerraformModuleService


class TerraformModule(BaseController):
    def __init__(self, service: TerraformModuleService):
        self.service = service

    def create(self, params):
        return self.service.create(params)

