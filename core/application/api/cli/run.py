from core.application.api.base import BaseAPIRunner
from core.application.api.cli.executors import *

TF_TEMPLATE_PARSER = 'tf_module_template'
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
        executors_dict = {executor.parser_name(): executor
                          for executor in EXECUTORS}
        subparsers = self.parser.add_subparsers()

        tf_template_sub_parser = subparsers.add_parser(TF_TEMPLATE_PARSER)
        tf_template_sub_parser.set_defaults(parser=TF_TEMPLATE_PARSER)
        tf_template_subparsers = tf_template_sub_parser.add_subparsers()

        tf_module_sub_parser = subparsers.add_parser(TF_MODULE_PARSER)
        tf_module_sub_parser.set_defaults(parser=TF_MODULE_PARSER)

        for executor in EXECUTORS:
            executor(tf_template_subparsers.add_parser(
                executor.parser_name())).init_cli_parser()
        args = vars(self.parser.parse_known_args()[0])
        parser = args.pop("parser", "")
        if not parser:
            self.parser.print_help()
            exit()
        action = args.pop("which", "")
        if not action:
            if parser == TF_TEMPLATE_PARSER:
                tf_template_sub_parser.print_help()
            if parser == TF_MODULE_PARSER:
                tf_module_sub_parser.print_help()
            exit()
        print(executors_dict.get(action).execute(self.service, **args))
