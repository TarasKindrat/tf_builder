from argparse import ArgumentParser

from core.application.api.cli.run import CLIApiRunner
from core.application.api.rest.run import RestAPIRunner
from core.application.services.terraform_module_service import TerraformModuleService
from core.application.services.terraform_module_template_service import TerraformModuleTemplateService
from core.infrastructure.repositories.terraform_module_repo import LocalTerraformModuleRepository
from core.infrastructure.repositories.terraform_module_template_repo import LocalTerraformModuleTemplateRepository


def run():
    local_terraform_module_template_repository = LocalTerraformModuleTemplateRepository()
    local_terraform_module_repository = LocalTerraformModuleRepository()
    template_service = TerraformModuleTemplateService(local_terraform_module_template_repository)
    module_service = TerraformModuleService(local_terraform_module_repository, template_service)

    parser = ArgumentParser(description='Terraform builder')
    runners = {
        'cli': CLIApiRunner(parser, template_service, module_service),
        'rest': RestAPIRunner(template_service, module_service),
    }

    parser.add_argument('command', help='Cli interface', choices=runners.keys())
    args = parser.parse_known_args()[0]

    runners.get(args.command).run()


if __name__ == '__main__':
    run()
