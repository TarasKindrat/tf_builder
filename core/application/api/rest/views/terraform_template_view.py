import json

from flask import jsonify, request
from flask_restful import Resource

from core.application.api.rest.helpers.request import get_request_params
from core.application.api.rest.helpers.response import make_api_response
from core.application.services.terraform_template_service import \
    TerraformTemplateService


class TerraformModuleTemplatesView(Resource):
    def __init__(self, service: TerraformTemplateService):
        self.service = service

    @make_api_response()
    def get(self):
        return jsonify({
            "modules": self.service.list(),
        })

    @make_api_response()
    def post(self):
        params = get_request_params(request)
        name = params.get("name")
        template = params.get("template", params.get("template_file"))
        variables = params.get("variables", params.get("variables_file"))
        if variables:
            variables = variables if isinstance(variables, dict) else json.loads(variables)
        return self.service.create(name, template, variables)


class TerraformModuleTemplateView(Resource):
    def __init__(self, service: TerraformTemplateService):
        self.service = service

    @make_api_response()
    def get(self, name):
        return jsonify(self.service.get(name))

    @make_api_response()
    def put(self, name):
        return 'update'

    @make_api_response()
    def delete(self, name):
        return "delete"
