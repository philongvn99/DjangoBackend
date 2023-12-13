import os
from dotenv import load_dotenv
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import json
import requests

from common import support as sp,  exceptions as exc
from . import models, forms, serializers as sr
# Create your views here.
# ALL PLAYER INFOs          ===============================================================

load_dotenv() 

# USER LOGIN / SIGNUP / MODIFY  ===============================================================
@api_view(["GET", "POST"])
def UserLogin(request):
    if request.method == "GET":
        return render(
            request, 
            'my_template.html',
            {  'form' : forms.LoginInfoForm(), 'url_name': "Log In" }
        )

    if request.method == "POST":
        userLoginInfo = forms.LoginInfoForm(request.data)
        # Valid Input
        if userLoginInfo.is_valid():
            response = requests.post(f'{os.getenv("FIREBASE_HOST")}/authentication/login/', data=userLoginInfo.data, verify=True)
            if response:
                return Response(response.json(), status=status.HTTP_200_OK)
            raise exc.UnprocessableEntity
        # Invalid Input
        else:
            print(userLoginInfo.errors)
            raise exc.InvalidInput


@api_view(["POST"])
def UserRegister(request):
    if request.method == "POST":
        userResInfo = forms.UserInfoForm(request.data)
        if not userResInfo.is_valid():
            response = models.submitUserLoginData(userResInfo.data)
            return Response(
                {"success": response["username"] != None, "userInfo": response},
                status=status.HTTP_200_OK
                if response != []
                else status.HTTP_401_UNAUTHORIZED,
            )
        # Valid Input
        else:           
            jsonStr = json.loads(userResInfo.errors.as_json())
            sp.displayError(jsonStr)
            return Response(
                {"success": False, "data": jsonStr},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )


@api_view(["GET", "PUT"])
def UserInfo(request, username):

    # GET User Information
    if request.method == "GET":
        response = models.getUserInfo(username)
        if response["username"] != None:
            return Response({"success": True, "userInfo": response}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False}, status=status.HTTP_204_NO_CONTENT)

    # UPDATE User Information
    elif request.method == "PUT":
        response = models.modifyUserInfo(request.data)
        print(response)
    
    
# expToken = eyJhbGciOiJSUzI1NiIsImtpZCI6ImQwZTFkMjM5MDllNzZmZjRhNzJlZTA4ODUxOWM5M2JiOTg4ZjE4NDUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiaG9sdGJ5MzMxIiwicGljdHVyZSI6Imh0dHBzOi8vZmlyZWJhc2VzdG9yYWdlLmdvb2dsZWFwaXMuY29tL3YwL2IvcGxmaXJlYmFzZS1jYzFmMS5hcHBzcG90LmNvbS9vL2FwaGVsaW9zLnBuZz9hbHQ9bWVkaWEiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcGxmaXJlYmFzZS1jYzFmMSIsImF1ZCI6InBsZmlyZWJhc2UtY2MxZjEiLCJhdXRoX3RpbWUiOjE2ODUxODk1OTgsInVzZXJfaWQiOiJ0S2g3Z0dIZmY5TlVnbFl4ZTkzMWdlNDlnQXEyIiwic3ViIjoidEtoN2dHSGZmOU5VZ2xZeGU5MzFnZTQ5Z0FxMiIsImlhdCI6MTY4NTE4OTU5OCwiZXhwIjoxNjg1MTkzMTk4LCJlbWFpbCI6ImhvbHRieTMzMUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInBob25lX251bWJlciI6Iis4NDMyNzA3MTk4NSIsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsicGhvbmUiOlsiKzg0MzI3MDcxOTg1Il0sImVtYWlsIjpbImhvbHRieTMzMUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.PB4ZznaTbzSAWJ8zobbENIgVd9J8MANAWsH0cRICs5TigdQJuTj17tX8Cr9RBWN2XfRImIpwFY5e1WznKVrGwOpjSrM5-Kig6vlqCVzMfOk2MN0Jp1Dj7BKR9ZCAb4EcaPV3IItMivDNiM9snqUCitkhUvfQbYC3Otdt9pEs_4k2CDX0GEGtpxcfuAMJP-bUqYMjDb9f7qiZUIucZScwpqdR3epoxBeoKNBZGFXBSTkYlXH406uVxuPs20KSxlV6Ca8WWF6vYvLNVqGT-3ZoinxExLUwixPCPpvBqU5iJfkabVYyHE23My_sDSRdDszFynBZd6EkOhQIY7782D0RPA