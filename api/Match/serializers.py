from rest_framework import serializers

from api.Match import models
from api.Team.serializers import RelatedTeamAttendanceSerializer


class MatchSerializer(serializers.ModelSerializer):
    home = RelatedTeamAttendanceSerializer()
    away = RelatedTeamAttendanceSerializer()

    class Meta:
        model = models.Match
        fields = "__all__"
