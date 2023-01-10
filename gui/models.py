from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class Dragon(models.Model):
    name = models.CharField(max_length=80)
    hp = models.IntegerField(default=1)
    attack = models.IntegerField(default=1)
    defense = models.IntegerField(default=1)
    speed = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    for_sale = models.BooleanField(default=False)
    type = models.IntegerField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=NULL, related_name='owner')
    shared_to = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField(default=1000)

    def __str__(self):
        return self.user.username

class Fight(models.Model):
    dragon_winner_owner = models.ForeignKey(User, on_delete=models.CASCADE, default=NULL,related_name='dragon_winner_owner_pk')
    dragon_loser_owner = models.ForeignKey(User, on_delete=models.CASCADE, default=NULL, related_name='dragon_loser_owner_pk')
    dragon_winner_name = models.CharField(max_length=80)
    dragon_loser_name = models.CharField(max_length=80)
    stolen_money = models.IntegerField(default=0)
    rounds = models.IntegerField(default=0)

    def __str__(self):
        return self.dragon_winner_name

    