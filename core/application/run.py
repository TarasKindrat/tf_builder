from flask import request, Flask, jsonify

from core.application.controllers.terraform_module import TerraformModule
from core.application.controllers.terraform_template import TerraformTemplate
from core.application.helpers.request import get_request_params
from core.version import api_version


def register_endpoint(
        app, endpoint=None, endpoint_name=None, handler=None, method=None):
    app.add_url_rule(endpoint, endpoint_name, handler, methods=[method])


def register_get_endpoint(
        app, endpoint=None, endpoint_name=None, handler=None):
    app.add_url_rule(endpoint, endpoint_name, handler, methods=['GET'])


def register_post_endpoint(
        app, endpoint=None, endpoint_name=None, handler=None):
    app.add_url_rule(endpoint, endpoint_name, handler, methods=['POST'])


def register_put_endpoint(
        app, endpoint=None, endpoint_name=None, handler=None):
    app.add_url_rule(endpoint, endpoint_name, handler, methods=['PUT'])


def register_delete_endpoint(
        app, endpoint=None, endpoint_name=None, handler=None):
    app.add_url_rule(endpoint, endpoint_name, handler, methods=['DELETE'])


class FlaskApp(object):
    _app = None

    def __init__(self):
        raise Exception('call instance()')

    @classmethod
    def app(cls):
        if cls._app is None:
            cls._app = Flask(__name__)
        return cls._app


class FlaskRunner(object):

    def __init__(
            self,
            terraform_template: TerraformTemplate,
            terraform_module: TerraformModule
    ):
        self.tf_template = terraform_template
        self.tf_module = terraform_module
        self.app = FlaskApp.app()

    def register_tf_template_endpoints(self):
        base_url = f'/api/{api_version}/templates'
        named_url = f'{base_url}/<string:name>'
        register_get_endpoint(
            self.app, base_url, "list_templates", self.tf_template.list)
        register_get_endpoint(
            self.app, named_url, "get_template", self.tf_template.get)
        register_post_endpoint(
            self.app, f'{base_url}', "create_template",
            lambda *args, **kwargs:
            self.tf_template.create(get_request_params(request)))
        register_put_endpoint(
            self.app, named_url, "update_template",
            lambda n, *args, **kwargs:
            self.tf_template.update(n, get_request_params(request)))
        register_delete_endpoint(
            self.app, named_url, "delete_template", self.tf_template.delete)

    def register_tf_module_endpoints(self):
        base_url = f'/api/{api_version}/modules'
        register_post_endpoint(
            self.app, f'{base_url}', "create_module",
            lambda: self.tf_module.create(request.get_json()))

    def run(self):
        self.register_tf_template_endpoints()
        self.register_tf_module_endpoints()

        @self.app.route('/')
        def index():
            urls = [' - '.join([i.rule, str(i.methods), i.endpoint])
                    for i in vars(self.app.url_map).get('_rules')]
            return jsonify(
                {'urls': sorted(urls, key=lambda x: (len(x.split('-')[0])))})

        self.app.run(debug=True)
