import json

from core.application.run import FlaskApp
from core.version import api_version


class GitTerraformModule(object):
    def __init__(self):
        self.app = FlaskApp.app()

    def create(self, params):
        return self.app.test_client().post(
            f'/api/{api_version}/modules', data=json.dumps(params),
            content_type='application/json').data