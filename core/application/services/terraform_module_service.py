import jinja2schema
from marshmallow import fields, ValidationError, validate

from core.application.services.base import BaseService
from core.application.services.terraform_template_service import \
    TerraformTemplateService
from core.domain.entities.base import BaseEntity
from core.domain.entities.terraform_module import TerraformModuleEntity
from core.domain.repositories.terraform_module_repo import \
    BaseTerraformModuleRepository


class VariablesValidationError(Exception):
    pass


class VariablesValidationService(BaseService):
    class SimpleField(fields.Field):
        def __init__(self, types, *args, **kwargs):
            self.types = types
            super(VariablesValidationService.SclarField, self).__init__(
                *args, **kwargs)

        def _deserialize(self, value, attr, data, **kwargs):
            if isinstance(value, str) or isinstance(value, list):
                return value
            else:
                raise ValidationError('Field should be str or list')

    def init_simple(self, item, result, title, append_to_result=True):
        types = [i.get('type') for i in item.get('anyOf')]
        if not append_to_result:
            return VariablesValidationService.SimpleField(types, required=True)
        result[title] = VariablesValidationService.SimpleField(types, required=True)

    def init_object(self, item, result, title, prefix):
        params = self.generate_vars_dataclass(item, nested=True, prefix=prefix)
        result[title] = fields.Nested(
            type(f"{prefix}Class", (BaseEntity,), params), required=True)

    def init_list(self, item, result, title, prefix):
        nested = item.get('items').get('type') == 'object'
        validation = validate.Length(min=1)
        obj = self.generate_vars_dataclass(
            item.get('items'), resut_append=nested, prefix=prefix)
        l_item = fields.Nested(obj, required=True) if nested else obj
        result[title] = fields.List(l_item, required=True, validate=validation)

    def generate_vars_dataclass(
            self, template_vars, resut_append=True, nested=False, prefix=''):
        result = {}
        items = (template_vars.get('properties').values()
                 if 'properties' in template_vars else [template_vars])
        for item in items:
            title = item.get('title')
            item_type = item.get('type')
            prefix = prefix + title
            if item.get('anyOf'):
                params = self.init_simple(item, result, title, resut_append)
                if not resut_append:
                    return params
            elif item_type == 'object':
                self.init_object(item, result, title, prefix)
            elif item_type == 'array':
                self.init_list(item, result, title, prefix)
        return (result if nested
                else type("TemplateVarsCls", (BaseEntity,), result))


class TerraformModuleService(BaseService):
    def __init__(self, repo: BaseTerraformModuleRepository,
                 terraform_template_service: TerraformTemplateService):
        self.repo = repo
        self.terraform_template_service = terraform_template_service

    def get(self, modules):
        pass

    def create(self, modules):
        for module in modules:
            tf_module = TerraformModuleEntity().load(module)
            template = self.terraform_template_service.get(tf_module.name)
            variables = jinja2schema.infer(template)
            vars = jinja2schema.to_json_schema(variables)
            if vars.get('properties'):
                if module.get('variables') is None:
                    raise VariablesValidationError(f"variables param is not provided for '{tf_module.name}' module")
                try:
                    vars_schema = (
                        VariablesValidationService()
                            .generate_vars_dataclass(vars))
                    vars_schema().load(module.get('variables'))
                except ValidationError as ex:
                    raise VariablesValidationError(f'module: {tf_module.name}', ex)

        return self.repo.create(modules, self.terraform_template_service)

    def delete(self, name):
        pass

    def update(self, name, template, variables):
        pass
