from core.application.api.base import BaseAPIRunner
from core.application.api.cli.executors import *

TF_MODULE_TEMPLATE_PARSER = 'tf_module_template'
TF_MODULE_PARSER = 'tf_module'
EXECUTORS = [
    TFTemplateGetExecutor,
    TFTemplateListExecutor,
    TFTemplateCreateExecutor,
    TFTemplateDeleteExecutor,
]


class CLIApiRunner(BaseAPIRunner):
    def __init__(self, parser, *args, **kwargs):
        super(CLIApiRunner, self).__init__(*args, **kwargs)
        self.parser = parser

    def run(self):
        executors_dict = {executor.parser_name(): executor for executor in EXECUTORS}
        subparsers = self.parser.add_subparsers()

        tf_module_template_subparser = subparsers.add_parser(TF_MODULE_TEMPLATE_PARSER)
        tf_module_template_subparser.set_defaults(parser=TF_MODULE_TEMPLATE_PARSER)
        tf_module_template_subparsers = tf_module_template_subparser.add_subparsers()

        tf_module_subparser = subparsers.add_parser(TF_MODULE_PARSER)
        tf_module_subparser.set_defaults(parser=TF_MODULE_PARSER)
        tf_module_subparsers = tf_module_subparser.add_subparsers()

        for executor in EXECUTORS:
            executor(tf_module_template_subparsers.add_parser(executor.parser_name())).init_cli_parser()
        args = vars(self.parser.parse_known_args()[0])
        parser = args.pop("parser", "")
        if not parser:
            self.parser.print_help()
            exit()
        action = args.pop("which", "")
        if not action:
            if parser == TF_MODULE_TEMPLATE_PARSER:
                tf_module_template_subparser.print_help()
            if parser == TF_MODULE_PARSER:
                tf_module_subparser.print_help()
            exit()
        print(executors_dict.get(action).execute(self.service, **args))
