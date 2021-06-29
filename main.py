from argparse import ArgumentParser

from core.application.api.cli.run import CLIApiRunner
from core.application.api.rest.run import RestAPIRunner
from core.application.services.terraform_module_service import TerraformModuleService
from core.application.services.terraform_module_template_service import TerraformModuleTemplateService
from core.infrastructure.repositories.terraform_module_repo import LocalTerraformModuleRepository
from core.infrastructure.repositories.terraform_module_template_repo import LocalTerraformModuleTemplateRepository
from core.infrastructure.repositories.terraform_module_template_repo import GitTerraformModuleTemplateRepository
from core.infrastructure.repositories.git_repo import GitRepository
def run():
    url ='git@github.com:zhhuta/test-tf-org.git'
    git_repo = GitRepository('/Users/zhhuta/PycharmProjects/tf_builder/test-tf-org/',user_name='zhhuta',password='', repo_url=url)
    git_terraform_module_template_repository = GitTerraformModuleTemplateRepository(git_repo, 'static')
    local_terraform_module_repository = LocalTerraformModuleRepository()
    template_service = TerraformModuleTemplateService(git_terraform_module_template_repository)
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
