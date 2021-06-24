import pprint


class BaseExecutor(object):
    def __init__(self, parser):
        self.parser = parser
        self.parser.set_defaults(which=self.__class__.parser_name())

    def init_cli_parser(self):
        raise NotImplementedError

    @staticmethod
    def execute(service, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def parser_name():
        return


class TFTemplateGetExecutor(BaseExecutor):

    def init_cli_parser(self):
        self.parser.add_argument("name")

    @staticmethod
    def execute(service, *args, **kwargs):
        return pprint.pformat(service.get(kwargs.get('name')), indent=4)

    @staticmethod
    def parser_name():
        return "get"


class TFTemplateListExecutor(BaseExecutor):

    def init_cli_parser(self):
        pass

    @staticmethod
    def execute(service, *args, **kwargs):
        return f'Available templates:\n  {"  ".join(service.list())}'

    @staticmethod
    def parser_name():
        return "list"


class TFTemplateCreateExecutor(BaseExecutor):

    def init_cli_parser(self):
        self.parser.add_argument('--name', required=True)
        self.parser.add_argument('--template', required=True)
        self.parser.add_argument('--vars', required=True)

    @staticmethod
    def execute(service, *args, **kwargs):
        return service.create(kwargs.get('name'), kwargs.get('template'), kwargs.get('vars'))

    @staticmethod
    def parser_name():
        return "create"


class TFTemplateUpdateExecutor(BaseExecutor):

    def init_cli_parser(self):
        self.parser.add_argument('--name', required=True)
        self.parser.add_argument('--template', required=True)
        self.parser.add_argument('--vars', required=True)

    @staticmethod
    def execute(service, *args, **kwargs):
        return service.update(kwargs.get('name'), kwargs.get('template'))

    @staticmethod
    def parser_name():
        return "update"


class TFTemplateDeleteExecutor(BaseExecutor):

    def init_cli_parser(self):
        self.parser.add_argument("name")

    def execute(self, service, *args, **kwargs):
        return pprint.pformat(service.delete(kwargs.get('name')), indent=4)

    @staticmethod
    def parser_name():
        return "delete"

