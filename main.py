from argparse import ArgumentParser

from core.application.api.cli.run import CLIApiRunner
from core.application.api.rest.run import RestAPIRunner
from core.application.services import TerraformModuleService
from core.infrastructure.repositories.terraform_module_template_repo import LocalTerraformModuleTemplateRepository


def run():
    local_terraform_module_repository = LocalTerraformModuleTemplateRepository()
    service = TerraformModuleService(local_terraform_module_repository)

    parser = ArgumentParser(description='Terraform builder')
    runners = {
        'cli': CLIApiRunner(parser, service),
        'rest': RestAPIRunner(service),
    }

    parser.add_argument('command', help='Cli interface', choices=runners.keys())
    args = parser.parse_known_args()[0]

    runners.get(args.command).run()


if __name__ == '__main__':
    run()
