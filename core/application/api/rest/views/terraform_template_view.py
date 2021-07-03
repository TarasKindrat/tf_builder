from flask import jsonify, request
from flask_restful import Resource

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

    # @make_api_response()
    def post(self):
        params = request.get_json()
        return self.service.create(
            params.get('name'),
            params.get('template'),
            params.get('variables')
        )


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
