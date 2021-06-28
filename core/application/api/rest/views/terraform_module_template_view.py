from flask import jsonify, request
from flask_restful import Resource

from core.application.services.terraform_module_template_service import TerraformModuleTemplateService


class TerraformModuleTemplatesView(Resource):
    def __init__(self, service: TerraformModuleTemplateService):
        self.service = service

    def get(self):
        return jsonify({
            "modules": self.service.list(),
        })

    def post(self):
        params = request.get_json()
        return self.service.create(params.get('name'), params.get('template'), params.get('var'))


class TerraformModuleTemplateView(Resource):
    def __init__(self, service: TerraformModuleTemplateService):
        self.service = service

    def get(self, name):
        return jsonify(self.service.get(name))

    def put(self, name):
        return 'update'

    def delete(self, name):
        return "delete"
