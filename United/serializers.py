from rest_framework import serializers
from . import support as sp, models

class PlayerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Player
        fields = sp.playerFields
        
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = '__all__'
    def __str__(self):
        return self.team_name
    
# class GroupStageTeamSerializer(serializers.ModelSerializer):
#     team = TeamSerializer()
#     class Meta:
#         model = models.GroupStageTeam
#         fields = ['team_id', 'group_stage_team_id', 'team_league', 'team', 'team__team_name'] 

