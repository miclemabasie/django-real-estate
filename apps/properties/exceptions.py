from rest_framework.exceptions import APIException


class PropertyNotFound(APIException):
    status = 404
    default_detail = "The requested property does not exist!"
