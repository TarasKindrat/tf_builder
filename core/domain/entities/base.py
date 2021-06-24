from marshmallow import Schema, EXCLUDE


class BaseTFBuilderException(Exception):
    """Base Terraform Builder Exception"""
    pass


class BaseEntity(Schema):
    """Base entity"""
    class Meta:
        """Filtering out unknown fields, providing error grouping"""
        index_errors = True
        unknown = EXCLUDE
