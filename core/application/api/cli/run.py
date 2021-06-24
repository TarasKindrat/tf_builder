import pprint

from core.application.api.base import BaseAPIRunner
from argparse import ArgumentParser


class CLIApiRunner(BaseAPIRunner):
    def run(self):
        parser = ArgumentParser(description='Terraform builder cli interface')
        parser.add_argument('--list', help='List possible terraform modules', action="store_true")
        parser.add_argument('--get', help='Get terraform module')
        args = parser.parse_known_args()[0]
        result = None
        if not [i for i in vars(args).values() if i]:
            parser.print_help()
            exit()
        if args.list:
            templates = "\n  ".join(self.service.list())
            result = f'Available templates:\n  {templates}'
        if args.get:
            result = pprint.pformat(self.service.get(args.get), indent=4)
        print(result)
