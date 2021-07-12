from core.application.controllers.terraform_module import TerraformModule
from core.application.controllers.terraform_template import TerraformTemplate
from core.application.run import FlaskRunner
from core.application.services.terraform_module_service import \
    TerraformModuleService
from core.application.services.terraform_template_service import \
    TerraformTemplateService
from core.infrastructure.repositories.terraform_module_repo import \
    LocalTerraformModuleRepository
from core.infrastructure.repositories.terraform_template_repo import \
    GitTerraformTemplateRepository
from core.infrastructure.repositories.git_repo import GitRepository
import os
from configparser import ConfigParser

from core.plugins import Plugin


def get_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'core', 'configs', 'main.ini')
    credential_path = os.path.join(dir_path, 'core', 'credentials', 'main.ini')
    config = ConfigParser()
    config.read(config_path)
    config.read(credential_path)
    return config


def run():
    git_config = get_config()['git']

    url = git_config.get('repo_url')
    git_path = git_config.get("repo_path")
    git_user = git_config.get("username")
    git_password = git_config.get("password")
    project_name = url.split('/')[-1].split('.')[0]
    template_dir = 'static/'

    repo = GitRepository(
        f"{git_path}{project_name}", git_user, git_password, url)
    tf_template_repository = GitTerraformTemplateRepository(repo, template_dir)
    template_service = TerraformTemplateService(tf_template_repository)
    template_controller = TerraformTemplate(template_service)

    tf_module_repository = LocalTerraformModuleRepository()
    module_service = TerraformModuleService(
        tf_module_repository, template_service)
    module_controller = TerraformModule(module_service)

    FlaskRunner(template_controller, module_controller).run()


if __name__ == '__main__':
    Plugin.load_plugins('plugins')
    run()
