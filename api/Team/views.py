import json
from django.apps import apps

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from src.common import exceptions as exc
from src.common import support as sp

from api.Team import forms
from api.Team import models
from api.Team import serializers


# Create your views here.
@api_view(["GET", "POST", "PUT", "DELETE"])
def Team(request):
    if request.method == "GET":
        models = {model for model in apps.get_app_configs()}
        print(models)
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


# EPL LEAGUE             ===============================================================
@api_view(["GET"])
def LeagueResult(request, date):
    if request.method == "GET":
        results = models.getLeagueResults(date)
        return Response(results, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "PUT", "DELETE"])
def LeagueTable(request, leagueId, season=2023):
    if request.method == "GET":
        leagueTeam = models.TeamAttendance.objects.filter(
            league_id=leagueId, season=season
        ).select_related("team")
        if leagueTeam == []:
            raise exc.ResourceNotFound
        return Response(
            serializers.TeamAttendanceSerializer(leagueTeam, many=True).data,
            status=status.HTTP_200_OK,
        )

    elif request.method == "POST":
        models.Team.objects.create(request.data)
        raise exc.ServiceUnavailable

    elif request.method == "PUT":
        matchResults = forms.MatchResultListForm(request.data)  # Validating INPUT
        if matchResults.is_valid():
            response = models.updateLeagueTable(
                request.data["id"],
                request.data["goalscore"],
                request.data["goalconceeded"],
                len(request.data["id"]),
            )
            return Response(response, status=status.HTTP_200_OK)

        json_string = json.loads(match_results.errors.as_json())
        sp.display_error(json_string)
        return Response(json_string, status=status.HTTP_406_NOT_ACCEPTABLE)

    return Response({}, status=status.HTTP_200_OK)
