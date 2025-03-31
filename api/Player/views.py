import json

from requests import Request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.Player import forms, models
from api.Player import serializers as sr
from common import constants as sp
from common import exceptions as exc

# Create your views here.
# ALL PLAYER INFOs          ===============================================================


@api_view(["GET", "POST"])
def all_player(request):
    if request.method == "GET":
        players = {}
        try:
            for position in sp.player_position:
                players[position + "s"] = models.Player.objects.filter(
                    role=position.upper()
                ).values()
            return Response(players, status=status.HTTP_200_OK)
        except Exception as e:
            raise e
    elif request.method == "POST":
        new_player_form = forms.NewPlayerForm(request.data or None)
        if new_player_form.is_valid():
            new_player = new_player_form.save()
            return Response(
                {**(new_player_form.cleaned_data), "id": new_player.id},
                status.HTTP_201_CREATED,
            )
        json_str = json.loads(new_player_form.errors.as_json())
        print(json_str)
        raise exc.InvalidInput(json_str)
    else:
        return Response({}, status.HTTP_200_OK)


# PLAYER INFOs BY POSITION  ===============================================================


@api_view(["GET"])
def player_by_position(request: Request, position):
    if request.method == "GET":
        if position not in sp.player_position:
            raise exc.ResourceNotFound
        players = models.Player.objects.filter(player_role=position.upper())
        serialized_player = sr.PlayerSerializer(players, many=True)
        return Response(serialized_player.data, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_200_OK)


# PLAYER INFO BY ID         ===============================================================


@api_view(["GET", "PUT", "DELETE"])
def player_by_id(request: Request, player_id):
    player = models.Player.objects.filter(id=player_id)
    if player:
        if request.method == "GET":
            serialized_player = sr.PlayerSerializer(player, many=True)
            return Response(serialized_player.data, status=status.HTTP_200_OK)
        if request.method == "PUT":
            updated_player = forms.UpdatePlayerForm(request.data or None)
            if updated_player.is_valid():
                # updatePlayer.save()
                player.update(**request.data)
                return Response({"message": "success"}, status=status.HTTP_200_OK)
            json_str = json.loads(updated_player.errors.as_json())
            raise exc.InvalidInput(json_str)
        if request.method == "DELETE":
            player.delete()
            return Response(player, status=status.HTTP_202_ACCEPTED)
    raise exc.ResourceNotFound
