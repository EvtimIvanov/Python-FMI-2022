from django.contrib import admin
from .models import Dragon, Fight, Player

# Register your models here.
class DragonAdmin(admin.ModelAdmin):
    model = Dragon
    search_fields = ('name',)
    list_display = ('name', 'hp','attack', 'defense', 'speed', 'price', 'for_sale', 'type', 'owner')
    fields = ('name', 'hp','attack', 'defense', 'speed', 'price', 'for_sale', 'type', 'owner')

class PlayerAdmin(admin.ModelAdmin):
    model = Player
    can_delete = False
    verbose_name_plural = 'player'
    list_display = ('user', 'money')

class FightAdmin(admin.ModelAdmin):
    model = Fight
    search_fields = ('dragon_winner_name',)
    list_display = ('dragon_winner_name', 'dragon_loser_name', 'dragon_winner_owner', 'dragon_loser_owner', 
    'stolen_money', 'rounds')

admin.site.register(Dragon, DragonAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Fight, FightAdmin)