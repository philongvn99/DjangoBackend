from rest_framework import serializers

from api.Team import models
from common import constants as sp


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = "__all__"


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.League
        fields = "__all__"


class TeamAttendanceSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = models.TeamAttendance
        fields = sp.teamAttendanceFields


class RelatedTeamAttendanceSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = models.TeamAttendance
        fields = ["team"]
