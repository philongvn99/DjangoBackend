from rest_framework import serializers

from api.Player import models
from src.common import support as sp


class PlayerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="id")
    name = serializers.CharField(source="name")
    full_name = serializers.CharField(source="full_name")
    avatar_link = serializers.CharField(source="avatar_link")
    nationality = serializers.CharField(source="nationality")
    birthday = serializers.CharField(source="birthday")
    right_foot = serializers.CharField(source="right_foot")
    kit_number = serializers.CharField(source="kit_number")
    height = serializers.CharField(source="height")
    role = serializers.CharField(source="role")
    salary = serializers.CharField(source="salary")
    status = serializers.CharField(source="status")

    class Meta:
        model = models.Player
        fields = sp.player_fields
