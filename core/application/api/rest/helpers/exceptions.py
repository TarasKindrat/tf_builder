""""Module holds exception related functionality, used in  microservice"""
# pylint:disable=line-too-long, broad-except, import-error, no-name-in-module, redefined-outer-name
from http import HTTPStatus
from typing import Dict, Tuple, Optional, Any

import marshmallow

from core.domain.entities.exception import TemplateNotFoundException, TemplateAlreadyExistException

API_ERRORS_DICT = {
    marshmallow.exceptions.ValidationError: ("Incorrect data in json: {}", HTTPStatus.BAD_REQUEST),
    TemplateNotFoundException: ("Template {} has not been found", HTTPStatus.NOT_FOUND),
    TemplateAlreadyExistException: ("Template {} already exists", HTTPStatus.BAD_REQUEST),
}


class APIExceptionHandler:
    """Context manager provides functionality to catch and log exceptions"""

    def __init__(self, exc_dict: Optional[Dict[Exception, Tuple[str, int]]] = None):
        """
        Accepting Dictionary with
        keys - Exception Type
        values - tuples (error string, error code)
        """
        self._exc_dict = API_ERRORS_DICT.copy()
        if exc_dict and isinstance(exc_dict, dict):
            self._exc_dict.update(exc_dict)
        self._output_err = None
        self._default = ("Error processing request: {}", HTTPStatus.INTERNAL_SERVER_ERROR)

    @property
    def error(self) -> Optional[Tuple[str, int, Exception, str, Any]]:
        """Getter for _output_error"""
        return self._output_err

    def __enter__(self):
        """Context manager enter"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit from context manager. If exception is in dictionary -  supressing exception and logging
        If not failing to default
        """
        self._output_err = ((self._exc_dict[exc_type][0], self._exc_dict[exc_type][1], exc_type, exc_val, exc_tb)
                            if exc_type in self._exc_dict.keys() else
                            (self._default[0], self._default[1], exc_type, exc_val, exc_tb))
        if not exc_type:
            self._output_err = None
        return True
