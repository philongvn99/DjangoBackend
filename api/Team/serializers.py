from rest_framework import serializers

from api.Team import models
from src.common import support as sp


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = "__all__"


class TeamAttendanceSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = models.TeamAttendance
        fields = sp.teamAttendanceFields
