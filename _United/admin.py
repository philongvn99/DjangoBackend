from django.contrib import admin
from Player.models import Player
from Team.models import Team, TeamAttendance

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(TeamAttendance)
