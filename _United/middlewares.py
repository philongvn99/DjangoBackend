from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from common import support as sp, exceptions as exc
from rest_framework import status
from firebase_admin import auth
import re


class JwtHandlerMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_urls = [
            re.compile(r"^/admin"),
            re.compile(r'^/auth'),
        ]
        # One-time configuration and initialization.

    def __call__(self, request):
        for pattern in self.exclude_urls:
            if pattern.match(request.path_info):
                return self.get_response(request)

        header_authorization_value = request.META.get("HTTP_AUTHORIZATION")
        if not header_authorization_value:
            raise exc.NoAuthToken
            
        match = sp.regex_bearer.match(header_authorization_value)
        if not match:
            raise exc.NoAuthToken
        
        firebase_jwt = match.groups()[-1]
        try:
            decoded_token = auth.verify_id_token(firebase_jwt)
            uid = decoded_token.get("uid")
            print(f'Request from user ${uid}')
        except Exception as e:
            return JsonResponse(data={'message': 'ExpiredToken' , 'detail': e.__str__()}, status=status.HTTP_401_UNAUTHORIZED)        
        response = self.get_response(request)
        return response

        
    def process_exception(self, request, exception):
        print('Exc Request is: r', request)
        return exception
    
    def process_response(self, request, response):
        print('Request is: ', request)
        print('Response is: ', response)
        return response