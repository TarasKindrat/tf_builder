from flask import Flask, jsonify
from flask_restful import Api

from core.application.api.base import BaseAPIRunner
from core.application.api.rest.views.terraform_module_view import TerraformModuleView, TerraformModulesView
from core.version import api_version


class RestAPIRunner(BaseAPIRunner):
    def run(self):
        app = Flask(__name__)

        @app.route('/')
        def index():
            return jsonify({
                'urls': list(set([str(i) for i in vars(app.url_map).get('_rules') if 'path:' not in str(i)]))})
        api = Api(app)
        api.add_resource(
            TerraformModulesView, f'/api/{api_version}/modules', resource_class_kwargs={'service': self.service})
        api.add_resource(
            TerraformModuleView, f'/api/{api_version}/modules/<string:name>', resource_class_kwargs={'service': self.service})
        app.run(debug=True)
