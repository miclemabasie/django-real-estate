from rest_framework.exceptions import APIException


class PropertyNotFound(APIException):
    status_code = 404
    default_detail = "Property not found."
    default_code = "property_not_found"
