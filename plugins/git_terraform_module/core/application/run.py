from flask import request
from core.application.run import FlaskApp
from core.version import api_version
from plugins.git_terraform_module.core.application.controllers.git_terraform_module import \
    GitTerraformModule


class FlaskRunner(object):

    def __init__(self):
        self.app = FlaskApp.app()

    def run(self):
        module = GitTerraformModule()
        self.app.add_url_rule(
            f'/api/{api_version}/git-modules',
            'create_module_git',
            lambda: module.create(request.get_json()),
            methods=['POST']
        )

