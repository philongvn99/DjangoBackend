from django.contrib import admin

from api.Player.models import Player, PlayerAdmin
from api.Match.models import Match, MatchAdmin, MatchEvent, MatchEventAdmin
from api.Team.models import Team, TeamAdmin

admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchEvent, MatchEventAdmin)
admin.site.register(Team, TeamAdmin)
