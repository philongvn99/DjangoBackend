from rest_framework import serializers

from common import support as sp
from . import models

class PlayerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='player_id')
    name = serializers.CharField(source='player_name')
    full_name = serializers.CharField(source='player_full_name')
    avatar_link = serializers.CharField(source='player_avatar_link')
    nationality = serializers.CharField(source='player_nationality')
    birthday = serializers.CharField(source='player_birthday')
    right_foot = serializers.CharField(source='player_right_foot')
    kit_number = serializers.CharField(source='player_kit_number')
    height = serializers.CharField(source='player_height')
    role = serializers.CharField(source='player_role')
    salary = serializers.CharField(source='player_salary')
    status = serializers.CharField(source='player_status')
    
    class Meta: 
        model = models.Player
        fields = sp.playerFields
