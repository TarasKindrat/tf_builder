from core.domain.entities.base import BaseTFBuilderException


class TemplateNotFoundException(BaseTFBuilderException):
    pass


class TemplateAlreadyExistException(BaseTFBuilderException):
    pass
