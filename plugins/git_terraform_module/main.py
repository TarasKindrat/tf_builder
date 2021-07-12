from core.plugins import BasePlugin
from plugins.git_terraform_module.core.application.run import FlaskRunner


class GitTerraformPlugin(BasePlugin):
    def run(self):
        FlaskRunner().run()
