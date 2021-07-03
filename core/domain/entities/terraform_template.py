from dataclasses import dataclass
import jinja2schema

from typing import Optional

from marshmallow import fields, validate, Schema, post_load

from core.domain.entities.base import BaseEntity


class DictField(fields.Field):

    def __init__(self, key_field, nested_field, *args, **kwargs):
        fields.Field.__init__(self, *args, **kwargs)
        self.key_field = key_field
        self.nested_field = nested_field

    def _deserialize(self, value, *args, **kwargs):
        ret = {}
        for key, val in value.items():
            k = self.key_field.deserialize(key)
            v = self.nested_field.deserialize(val)
            ret[k] = v
        return ret

    def _serialize(self, value, attr, obj):
        ret = {}
        for key, val in value.items():
            k = self.key_field._serialize(key, attr, obj)
            v = self.nested_field.serialize(key, self.get_value(attr, obj))
            ret[k] = v
        return ret


@dataclass
class TerraformTemplateVariableEntityDataclass(Schema):
    type: str
    help: str
    required: bool


@dataclass
class TerraformModuleTemplateEntityDataclass(Schema):
    name: str
    template: str
    variables: Optional[TerraformTemplateVariableEntityDataclass]


class TerraformTemplateVariableEntity(BaseEntity):
    """Core Terraform Module Template Entity"""
    type = fields.String(required=True)
    help = fields.String(required=True)
    required = fields.Boolean(required=True)


class TerraformModuleTemplateEntity(BaseEntity):
    """Core Terraform Module Template Entity"""
    name = fields.String(required=True)
    template = fields.String(required=True)
    variables = DictField(
        fields.Str(validate=validate.Regexp(r'^[a-zA-Z_]+$')),
        fields.Nested(TerraformTemplateVariableEntity),
        required=False, default={}, missing={}, allow_none=True
    )

    @post_load
    def make_dataclass(self, data, **kwargs):
        """Dumping model on correct load"""
        return TerraformModuleTemplateEntityDataclass(**data)
