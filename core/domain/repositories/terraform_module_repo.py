from abc import abstractmethod


class BaseTerraformModuleRepository(object):
    @abstractmethod
    def get(self, name):
        """ Get Terraform module
        :param name: module name
        :return: str
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, name, variables):
        """Create new terraform module
        :param name: str module name
        :param variables: dict
        :return: str
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, name, content):
        """Update existing terraform module
        :param name: module name
        :param content: content
        :return: str
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, name):
        """Delete terraform module
        :param name: name
        :return: str
        """
        raise NotImplementedError
