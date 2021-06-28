from http import HTTPStatus

from flask import request, make_response
from flask_restful import Resource

from core.application.api.rest.helpers.response import make_api_response
from core.application.services.terraform_module_service import TerraformModuleService


class TerraformModuleView(Resource):
    def __init__(self, service: TerraformModuleService):
        self.service = service

    @make_api_response()
    def get(self):
        return "get"

    @make_api_response()
    def post(self):
        modules = request.get_json()
        response = self.service.create(modules)
        resp = make_response(response, HTTPStatus.OK)
        resp.headers['Content-Type'] = "text/plain"
        return resp
