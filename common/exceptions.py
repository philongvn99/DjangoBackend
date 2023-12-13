from rest_framework.exceptions import APIException
from rest_framework import status


class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Service Temporarily Unavailable, try again later'
    default_code = 'service_unavailable'
    
    
class ResourceNotFound(APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = 'Resource is required NOT FOUND'
    default_code = 'resource_not_found'
    
class InvalidInput(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid Input format, please check and try again'
    default_code = 'invalid_input'
    
class UnprocessableEntity(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Invalid content of input, please check again'
    default_code = "invalid_content"
    
class NoAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "No authentication token provided"
    default_code = "no_auth_token"
    
class Unauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid Auth Token format (-B/bearer [CODE]- is required)"
    default_code ="unauthorized_user"
        
class InvalidAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid authentication token provided"
    default_code = "invalid_token"
        
class FirebaseError(APIException):
    def __init__(
            self, detail="The user provided with the auth token is not a valid Firebase user, it has no Firebase UID", 
            code="firebase_error"
        ):
        super().__init__(detail, code)
    status_code = status.HTTP_400_BAD_REQUEST,
