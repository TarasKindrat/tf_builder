from flask import Flask, jsonify
from flask_restful import Api

from core.application.api.base import BaseAPIRunner
from core.application.api.rest.views.terraform_template_view import (
    TerraformModuleTemplateView, TerraformModuleTemplatesView)
from core.application.api.rest.views.terraform_module_view import (
    TerraformModuleView)
from core.version import api_version


class RestAPIRunner(BaseAPIRunner):
    def run(self):
        app = Flask(__name__)

        @app.route('/')
        def index():
            urls = [str(i) for i in vars(app.url_map).get('_rules')
                    if 'path:' not in str(i)]
            return jsonify({'urls': list(set(urls))})

        api = Api(app)
        api.add_resource(
            TerraformModuleTemplatesView, f'/api/{api_version}/templates',
            resource_class_kwargs={'service': self.terraform_template_service})
        api.add_resource(
            TerraformModuleTemplateView,
            f'/api/{api_version}/templates/<string:name>',
            resource_class_kwargs={'service': self.terraform_template_service})
        api.add_resource(
            TerraformModuleView, f'/api/{api_version}/modules',
            resource_class_kwargs={'service': self.terraform_module_service})
        app.run(debug=True)
