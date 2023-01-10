from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index),
    path('login', auth_views.LoginView.as_view()),
    path('register', views.register),
    path('logout', auth_views.LogoutView.as_view()),
    path('my_sale', views.my_sale),
    path('market',views.market),
    path('remove_from_market/<int:dragonId>', views.remove_from_market),
    path('add_to_market/<int:dragonId>/price/<int:price>', views.add_to_market),
    path('buy_dragon/<int:dragonId>', views.buy_dragon),
    path('breed', views.breed),
    path('breed_dragons', views.breed_dragons),
    path('fight', views.fight_view),
    path('fight_dragons', views.fight),
    path('history', views.history)
]