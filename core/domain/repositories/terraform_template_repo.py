from abc import abstractmethod

from core.domain.entities.terraform_template import TerraformTemplateEntity


class BaseTerraformTemplateRepository(object):
    @abstractmethod
    def list(self):
        """List available Terraform Modules templates
        :return list
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, name):
        """ Get Terraform module template
        :param name: module name
        :return: str
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, terraform_template_entity: TerraformTemplateEntity):
        """Create new terraform module template
        :param terraform_template_entity: TerraformModuleTemplateEntity
        :return: TerraformModuleTemplateEntity
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, terraform_template_entity: TerraformTemplateEntity):
        """Update existing terraform module template
        :param terraform_template_entity: TerraformModuleTemplateEntity
        :return: TerraformModuleTemplateEntity
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, name):
        """Delete terraform module template
        :param name: name
        :return: str
        """
        raise NotImplementedError
