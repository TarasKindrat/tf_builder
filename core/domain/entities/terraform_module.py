from dataclasses import dataclass

from marshmallow import fields, post_load, Schema

from core.domain.entities.base import BaseEntity


@dataclass
class TerraformModuleEntityDataclass(Schema):
    name: str
    variables: dict


class TerraformModuleEntity(BaseEntity):
    """Core Terraform Module Template Entity"""
    name = fields.String(required=True)
    variables = fields.Dict(required=False, empty={}, missing={})

    @post_load
    def make_dataclass(self, data, **kwargs):
        """Dumping model on correct load"""
        return TerraformModuleEntityDataclass(**data)
