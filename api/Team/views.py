import json

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


# EPL LEAGUE             ===============================================================
@api_view(["GET"])
def league_result(request, date):
    if request.method == "GET":
        results = models.get_league_results(date)
        return Response(results, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "PUT", "DELETE"])
def league_table(request, league_id, season=2023):
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

    if request.method == "POST":
        models.Team.objects.create(request.data)
        raise exc.ServiceUnavailable

    if request.method == "PUT":
        match_results = forms.LeagueResultForm(request.data)  # Validating INPUT
        if match_results.is_valid():
            response = forms.update_league_table(match_results)
            return Response(response, status=status.HTTP_200_OK)

        json_string = json.loads(match_results.errors.as_json())
        sp.display_error(json_string)
        return Response(json_string, status=status.HTTP_406_NOT_ACCEPTABLE)

    return Response({}, status=status.HTTP_200_OK)
