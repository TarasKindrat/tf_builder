from abc import abstractmethod


class BaseTerraformModuleTemplateRepository(object):
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
    def get_variables(self, name):
        """ Get Terraform module expected variables
        :param name: module name
        :return: str
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, name, content):
        """Create new terraform module template
        :param name: str module name
        :param content: str jinja2 template
        :return: str
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, name, content):
        """Update existing terraform module template
        :param name: module name
        :param content: content
        :return: str
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, name):
        """Delete terraform module template
        :param name: name
        :return: str
        """
        raise NotImplementedError
