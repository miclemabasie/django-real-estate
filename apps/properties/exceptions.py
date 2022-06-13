from rest_framework.exceptions import ApiException


class PropertyNotFound(ApiException):
    status = 404
    default_detail ="The requested property does not exist!"

    