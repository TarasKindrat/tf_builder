from flask import jsonify
from flask_restful import Resource

from core.application.services import TerraformModuleService


class TerraformModuleTemplatesView(Resource):
    def __init__(self, service: TerraformModuleService):
        self.service = service

    def get(self):
        return jsonify({
            "modules": self.service.list(),
        })


class TerraformModuleTemplateView(Resource):
    def __init__(self, service: TerraformModuleService):
        self.service = service

    def get(self, name):
        return jsonify(self.service.get(name))
