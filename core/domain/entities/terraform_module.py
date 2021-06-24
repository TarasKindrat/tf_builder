from marshmallow import fields

from core.domain.entities.base import BaseEntity


class TerraformModuleEntity(BaseEntity):
    """Core Terraform Module Template Entity"""
    name = fields.String(required=True)
    variables = fields.String(required=True)
