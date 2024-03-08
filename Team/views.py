import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common import exceptions as exc
from common import support as sp

from . import forms, models, serializers


# Create your views here.
@api_view(["GET", "POST", "PUT", "DELETE"])
def Team(request):
    if request.method == 'POST':
        newTeam = forms.PlayerForm(request.data)
        if newTeam.is_valid():
            newTeam.save()
            return Response(newTeam.cleaned_data, status.HTTP_201_CREATED)
        else:
            jsonStr = json.loads(newTeam.errors.as_json())
            print(jsonStr)
            raise exc.InvalidInput(jsonStr)

# EPL LEAGUE             ===============================================================
@api_view(["GET"])
def LeagueResult(request, date):
    if request.method == "GET":
        results = models.getLeagueResults(date)
        return Response(results, status=status.HTTP_200_OK)
    

@api_view(["GET", "POST", "PUT", "DELETE"])
def LeagueTable(request, leagueId, season=2023):    
    if request.method == "GET":
        leagueTeam = models.TeamAttendance.objects.filter(
                league_id=leagueId,
                season=season
            ).select_related('team')
        if leagueTeam == []:
            raise exc.ResourceNotFound
        return Response(
            serializers.TeamAttendanceSerializer(leagueTeam, many=True).data, 
            status=status.HTTP_200_OK
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
                len(request.data["id"])
            )
            return Response(response, status=status.HTTP_200_OK)
        else:
            jsonStr = json.loads(matchResults.errors.as_json())
            sp.displayError(jsonStr)
            return Response(jsonStr, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    elif request.method == "DELETE":
        response = models.clearLeagueTable()
        return Response(response, status=status.HTTP_200_OK)


