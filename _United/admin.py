from django.contrib import admin
from Auth.models import Account
from Player.models import Player
from Team.models import Team, GroupStageTeam

admin.site.register(Player)
admin.site.register(Account)
admin.site.register(Team)
admin.site.register(GroupStageTeam)
