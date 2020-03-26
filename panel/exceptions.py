from rest_framework.exceptions import APIException


class IllegalOperation(APIException):
    status_code = 400
    default_detail = "Illegal operation"
    default_code = "illegal_operation"


class ValidationError(APIException):
    status_code = 400
    default_detail = "Validation Error"
    default_code = "validation_error"
