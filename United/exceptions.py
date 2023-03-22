from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service Temporarily Unavailable, try again later'
    default_code = 'service_unavailable'
    
    
class ResourceNotFound(APIException):
    status_code = 204
    default_detail = 'Resource is required NOT FOUND'
    default_code = 'resource_not_found'
    
class InvalidInput(APIException):
    status_code = 400
    default_detail = 'Invalid Input format, please check and try again'
    default_code = 'invalid_input'