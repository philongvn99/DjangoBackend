from django.core import serializers
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from . import models, forms, serializers as sr, support as sp, exceptions as exc

# Create your views here.
# ALL PLAYER INFOs          ===============================================================

@api_view(["GET", "POST"])
def AllPlayerInfo(request):
    if request.method == "GET":
        players = {}
        for position in sp.playerPosition:
            players[position + 's'] = sr.PlayerSerializer(
                    models.Player.objects.filter(player_role=position.upper()),
                    many=True
                ).data
        return Response(players, status=status.HTTP_200_OK)
    elif request.method == "POST":
        newPlayer = forms.PlayerForm(request.data or None)
        if newPlayer.is_valid():
            newPlayer.save()
            return Response(newPlayer.cleaned_data, status.HTTP_201_CREATED)
        else:
            jsonStr = json.loads(newPlayer.errors.as_json())
            raise exc.InvalidInput(jsonStr)

# PLAYER INFOs BY POSITION  ===============================================================

@api_view(["GET"])
def PlayerInfoByPosition(request, position):
    if request.method == "GET":
        if(position not in  sp.playerPosition):
            raise exc.ResourceNotFound
        playerByPosition = models.Player.objects.filter(player_role=position.upper())
        srPlayer = sr.PlayerSerializer(playerByPosition, many=True)
        return Response(srPlayer.data, status=status.HTTP_200_OK)

# PLAYER INFO BY ID         ===============================================================

@api_view(["GET", "PUT", "DELETE"])
def PlayerInfoByID(request, ID):
    playerByID = models.Player.objects.filter(player_id=ID)
    if playerByID:      
        if request.method == "GET":        
            srPlayer = sr.PlayerSerializer(playerByID, many=True)
            return Response(srPlayer.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":        
            if playerByID:      
                srPlayer = sr.PlayerSerializer(playerByID, many=True)
                return Response(srPlayer.data, status=status.HTTP_200_OK)
        elif request.method == "DELETE":        
            playerByID.delete()
            return Response(playerByID, status=status.HTTP_202_ACCEPTED)
    return exc.ResourceNotFound


# EPL LEAGUE             ===============================================================
@api_view(["GET"])
def LeagueResult(request, date):
    if request.method == "GET":
        results = models.getLeagueResults(date)
        return Response(results, status=status.HTTP_200_OK)
    

@api_view(["GET", "POST", "PUT", "DELETE"])
def LeagueTable(request, season=2023):    
    if request.method == "GET":
        leagueTeam = models.GroupStageTeam.objects.filter(
                team_league='PREMIER_LEAGUE',
                team_season=season
            ).select_related('base_team').values(*sp.leagueTableField)
        if leagueTeam == []:
            raise exc.ResourceNotFound
        return Response(leagueTeam, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
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
    
    

# REFRESH TOKEN ===============================================================================
@api_view(["GET", "POST"])
def UserRefreshToken(request):
    if request.method == "POST":
        if ('refresh_token' not in request.data.keys()):
            return Response({'success': False, 'message': 'Please send refresh_token'}, status=status.HTTP_400_BAD_REQUEST)
        new_access_Token = newAccessToken(request.data['refresh_token'])
        return Response({'success': True, 'accessToken': new_access_Token}, status=status.HTTP_200_OK)
    
    

# USER LOGIN / SIGNUP / MODIFY  ===============================================================
@api_view(["GET", "POST"])
def UserLogin(request):
    if request.method == "GET":
        x = forms.PlayerInfoForm(
            {"salary": 0} | {"name": "haha", "number": 1, "status": "A"}
        )
        for err in json.loads(x.errors.as_json()).items():
            print(err)
        return Response({"status": "OKE"}, status=status.HTTP_200_OK)

    if request.method == "POST":
        userLoginInfo = forms.LoginInfoForm(request.data)
        # Valid Input
        if userLoginInfo.is_valid():
            # TODO: Add implementation
            pass
        # Valid Input
        else:
            jsonStr = json.loads(userLoginInfo.errors.as_json())
            sp.displayError(jsonStr)
            return Response(
                {"success": False, "data": jsonStr},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )


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


@api_view(["GET", "POST"])
def test(request):
    return render(request, 'my_template.html', {'form' : forms.PlayerForm()})

# http://localhost:8000/UnitedHome/player/

# {
#   "player_name": "Sabitzer",
#   "player_full_name": "Marcel Sabitzer",
#   "player_nationality": "Austria",
#   "player_avatar_link": "https://resources.premierleague.com/premierleague/photos/players/250x250/p101338.png",
#   "player_birthday": "1994-03-17",
#   "player_right_foot": true,
#   "player_kit_number": 15,
#   "player_height": "178",
#   "player_role": "MIDFIELDER",
#   "player_salary": "211",
#   "player_stat": "ACTIVE"
# }