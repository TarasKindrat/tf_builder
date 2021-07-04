from abc import abstractmethod

from core.application.services.terraform_module_service import (
    TerraformModuleService)
from core.application.services.terraform_template_service import (
    TerraformTemplateService)


class BaseAPIRunner(object):
    def __init__(self, terraform_template_service: TerraformTemplateService,
                 terraform_module_service: TerraformModuleService):
        self.terraform_template_service = terraform_template_service
        self.terraform_module_service = terraform_module_service

    @abstractmethod
    def run(self):
        raise NotImplementedError
