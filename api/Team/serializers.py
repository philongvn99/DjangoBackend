from rest_framework import serializers

from api.Team import models
from src.common import support as sp
from . import models


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = "__all__"

    def __str__(self):
        return self.team_name


class TeamAttendanceSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = models.TeamAttendance
        fields = sp.teamAttendanceFields
