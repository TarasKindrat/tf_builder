from marshmallow import fields

from core.domain.entities.base import BaseEntity


class Git(BaseEntity):
    """Core Terraform Module Entity"""
    url = fields.String(required=True)
    path = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
