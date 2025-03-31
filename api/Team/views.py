import json

from django.db import transaction
from requests import Request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.Team import forms, models, serializers
from common import exceptions as exc


# Create your views here.
@api_view(["GET", "POST", "PUT", "DELETE"])
def team(request):
    if request.method == "GET":
        return {"message": "success"}
    if request.method == "POST":
        new_team = forms.NewTeamForm(request.data)
        if new_team.is_valid():
            new_team.save()
            return Response(new_team.cleaned_data, status.HTTP_201_CREATED)

        json_string = json.loads(new_team.errors.as_json())
        print(json_string)
        raise exc.InvalidInput(json_string)
    return Response({}, status=status.HTTP_200_OK)


@api_view(["GET"])
@transaction.atomic
def league_table(request: Request, league_id, season=2023):
    if request.method == "GET":
        league_team = models.TeamAttendance.objects.filter(
            league_id=league_id, season=season
        ).select_related("team")
        if league_team == []:
            raise exc.ResourceNotFound
        return Response(
            serializers.TeamAttendanceSerializer(league_team, many=True).data,
            status=status.HTTP_200_OK,
        )

    return Response({}, status=status.HTTP_200_OK)


@api_view(["GET"])
@transaction.atomic
def league(request: Request):
    if request.method == "GET":
        _league = models.League.objects.all()
        return Response(
            serializers.LeagueSerializer(_league, many=True).data,
            status=status.HTTP_200_OK,
        )
    return Response({}, status=status.HTTP_200_OK)
