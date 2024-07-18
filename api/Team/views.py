import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError, transaction

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
@transaction.atomic
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
        match_results = [
            forms.LeagueMatchResultForm(data) for data in request.data["results"]
        ]  # Validating INPUT

        if all(res.is_valid() for res in match_results):
            update_values = forms.convert_result_2_point(match_results)
            update_results = []
            sid = transaction.savepoint()

            try:
                with transaction.atomic():
                    for team_id, update_value in update_values.items():
                        team_att = models.TeamAttendance.objects.get(pk=team_id)

                        team_att.play += update_value.play
                        team_att.win += update_value.win
                        team_att.draw += update_value.draw
                        team_att.lost += update_value.lost
                        team_att.score += update_value.score
                        team_att.conceded += update_value.conceded

                        team_att.save()
                        update_results.append(team_att.clean())
            except IntegrityError:
                transaction.rollback(sid)
            return Response(update_results, status=status.HTTP_200_OK)

        json_string = json.loads(
            next(res for res in match_results if not res.is_valid()).errors.as_json()
        )
        sp.display_error(json_string)
        return Response(json_string, status=status.HTTP_400_BAD_REQUEST)

    return Response({}, status=status.HTTP_200_OK)
