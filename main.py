from argparse import ArgumentParser

from core.application.api.cli.run import CLIApiRunner
from core.application.api.rest.run import RestAPIRunner
from core.application.services.terraform_module_service import \
    TerraformModuleService
from core.application.services.terraform_template_service import \
    TerraformTemplateService
from core.infrastructure.repositories.terraform_module_repo import \
    LocalTerraformModuleRepository
from core.infrastructure.repositories.terraform_module_template_repo import \
    GitTerraformTemplateRepository
from core.infrastructure.repositories.git_repo import GitRepository
import os
from configparser import ConfigParser


def get_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'core', 'configs', 'main.ini')
    creds_path = os.path.join(dir_path, 'core', 'credentials', 'main.ini')
    config = ConfigParser()
    config.read(config_path)
    config.read(creds_path)
    return config


def run():
    git_config = get_config()['git']

    url = git_config.get('repo_url')
    git_path = git_config.get("repo_path")
    git_user = git_config.get("username")
    git_psswd = git_config.get("password")
    project_name = url.split('/')[-1].split('.')[0]
    templates_dir = 'static/'

    repo = GitRepository(f"{git_path}{project_name}", git_user, git_psswd, url)
    tf_template_repository = GitTerraformTemplateRepository(repo, templates_dir)
    template_service = TerraformTemplateService(tf_template_repository)

    tf_module_repository = LocalTerraformModuleRepository()
    module_service = TerraformModuleService(tf_module_repository, template_service)

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
