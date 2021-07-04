from dataclasses import dataclass
from marshmallow import fields, Schema, post_load

from core.domain.entities.base import BaseEntity


@dataclass
class TerraformModuleTemplateEntityDataclass(Schema):
    name: str
    template: str


class TerraformTemplateEntity(BaseEntity):
    """Core Terraform Module Template Entity"""
    name = fields.String(required=True)
    template = fields.String(required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        """Dumping model on correct load"""
        return TerraformModuleTemplateEntityDataclass(**data)
