from abc import abstractmethod

from core.application.services import TerraformModuleService


class BaseAPIRunner(object):
    def __init__(self, terraform_module_service: TerraformModuleService):
        self.service = terraform_module_service

    @abstractmethod
    def run(self):
        raise NotImplementedError
