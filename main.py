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
    url = "https://github.com/BohdanaKuzmenko/tf_tmp_repo.git"
    repo = GitRepository(f"/Users/zhhuta/PycharmProjects/{url.split('/')[-1].split('.')[0]}", "usr", "passw",
                         url)
    local_terraform_module_template_repository = GitTerraformModuleTemplateRepository(repo, 'static/templates')
    template_service = TerraformModuleTemplateService(local_terraform_module_template_repository)

    local_terraform_module_repository = LocalTerraformModuleRepository()
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
