from marshmallow import fields

from core.domain.entities.base import BaseEntity


class TerraformModuleTemplateEntity(BaseEntity):
    """Core Terraform Module Template Entity"""
    name = fields.String(required=True)
    template = fields.String(required=True)
    variables = fields.Dict(required=True)
