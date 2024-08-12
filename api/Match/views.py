import json
from urllib.request import Request

from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.Match import forms, models, serializers
from src.common import exceptions as exc, support as sp


# EPL LEAGUE             ===============================================================
@api_view(["GET"])
def league_result_by_round(request: Request, season: int, league_id: int, match_week=1):
    if request.method == "GET":
        matches = (
            models.Match.objects.filter(
                league_id=league_id,
                round=match_week,
                home__season=season,
                away__season=season,
            )
            .select_related("home")
            .select_related("away")
        )
        if len(matches) == 0:
            crawled_matches = models.get_epl_results_by_round(season, match_week)

            if len(crawled_matches) == 0:
                raise exc.ResourceNotFound

            team_attendances = dict(
                (team["team__acronym_name"], team["id"])
                for team in models.TeamAttendance.objects.filter(
                    league_id=league_id, season=season
                ).values("id", "team__acronym_name")
            )

            match_input = [
                models.Match(
                    home_id=team_attendances[match[2][0]],
                    away_id=team_attendances[match[2][1]],
                    external_id=match[0],
                    fthg=match[1][0],
                    ftag=match[1][1],
                    round=match_week,
                    league_id=league_id,
                )
                for match in crawled_matches
            ]

            sid = transaction.savepoint()
            try:
                with transaction.atomic():

                    matches = models.Match.objects.bulk_create(
                        match_input,
                        len(crawled_matches),
                    )

                    match_result_forms = [
                        forms.LeagueMatchResultForm(data.__dict__)
                        for data in match_input
                    ]  # Validating INPUT

                    if all(res.is_valid() for res in match_result_forms):
                        update_values = forms.convert_result_2_point(match_result_forms)

                        for team_id, update_value in update_values.items():
                            team_att = models.TeamAttendance.objects.get(pk=team_id)

                            team_att.play += update_value.play
                            team_att.win += update_value.win
                            team_att.draw += update_value.draw
                            team_att.lost += update_value.lost
                            team_att.score += update_value.score
                            team_att.conceded += update_value.conceded

                            team_att.save()

                        models.update_remote_dynamodb(season, match_week)

                    else:
                        json_string = json.loads(
                            next(
                                res for res in match_result_forms if not res.is_valid()
                            ).errors.as_json()
                        )
                        sp.display_error(json_string)
                        return Response(json_string, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError:
                transaction.rollback(sid)

        return Response(
            serializers.MatchSerializer(matches, many=True).data,
            status=status.HTTP_200_OK,
        )

    return Response({}, status=status.HTTP_200_OK)


@api_view(["GET"])
def match(request: Request, league_id: int, match_id: int):
    _match = (
        models.Match.objects.filter(
            league_id=league_id,
            id=match_id,
        )
        .select_related("home")
        .select_related("away")
    )
    if _match:
        if request.method == "GET":
            return Response(
                serializers.MatchSerializer(_match[0]).data,
                status=status.HTTP_200_OK,
            )
    return exc.ResourceNotFound
