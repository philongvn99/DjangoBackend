import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common import exceptions as exc
from common import support as sp

from . import forms, models
from . import serializers as sr

# Create your views here.
# ALL PLAYER INFOs          ===============================================================

@api_view(["GET", "POST"])
def AllPlayer(request):
    if request.method == "GET":
        players = {}
        try:
            for position in sp.playerPosition:
                players[position + 's'] = models.Player.objects.filter(role=position.upper()).values()
            return Response(players, status=status.HTTP_200_OK)
        except Exception as e:
            raise e
    elif request.method == "POST":
        newPlayer = forms.NewPlayerForm(request.data or None)
        if newPlayer.is_valid():
            newPlayer.save()
            return Response(newPlayer.cleaned_data, status.HTTP_201_CREATED)
        else:
            jsonStr = json.loads(newPlayer.errors.as_json())
            print(jsonStr)
            raise exc.InvalidInput(jsonStr)

        
    

# PLAYER INFOs BY POSITION  ===============================================================

@api_view(["GET"])
def PlayerByPosition(request, position):
    if request.method == "GET":
        if(position not in  sp.playerPosition):
            raise exc.ResourceNotFound
        playerByPosition = models.Player.objects.filter(player_role=position.upper())
        srPlayer = sr.PlayerSerializer(playerByPosition, many=True)
        return Response(srPlayer.data, status=status.HTTP_200_OK)

# PLAYER INFO BY ID         ===============================================================

@api_view(["GET", "PUT", "DELETE"])
def PlayerByID(request, ID):
    playerByID = models.Player.objects.filter(id=ID)
    if playerByID:      
        if request.method == "GET":        
            srPlayer = sr.PlayerSerializer(playerByID, many=True)
            return Response(srPlayer.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":   
            updatePlayer = forms.UpdatePlayerForm(request.data or None)
            if updatePlayer.is_valid():
                # updatePlayer.save()
                playerByID.update(**request.data)
                return Response({"message": 'success'}, status=status.HTTP_200_OK)
            else:
                jsonStr = json.loads(updatePlayer.errors.as_json())
                raise exc.InvalidInput(jsonStr)     
        elif request.method == "DELETE":        
            playerByID.delete()
            return Response(playerByID, status=status.HTTP_202_ACCEPTED)
    return exc.ResourceNotFound


