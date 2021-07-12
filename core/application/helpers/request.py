class BaseRequestParamException(Exception):
    pass


class FileExtensionException(BaseRequestParamException):
    pass


def validate_file_extension(file_name):
    allowed_extensions = ['json', 'jinja2']
    if file_name.split('.')[-1] not in allowed_extensions:
        raise FileExtensionException(file_name)


def get_request_params(request):
    params = {}
    if request.args:
        params.update(dict(request.args))
    if request.get_json():
        params.update(request.get_json())
    if request.form:
        params.update(dict(request.form))
    if request.files:
        for f in request.files:
            validate_file_extension(request.files[f].filename)
            params[f] = str(request.files[f].stream.read(), 'utf-8')
    return params
