from core.domain.repositories.terraform_module_repo import BaseTerraformModuleRepository


class TerraformModuleRepository(BaseTerraformModuleRepository):
    def get(self, name):
        pass

    def create(self, name, variables):
        pass

    def update(self, name, content):
        pass

    def delete(self, name):
        pass
