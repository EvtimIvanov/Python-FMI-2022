from django.test import Client, TestCase
from django.urls import resolve, reverse
from gui.models import Dragon, Player
from django.contrib.auth.models import User
from gui.views import create_dragon, damage, fight, generate_stat, start_fight, transfer_stolen_money, validate_if_dragons_can_fight

class YourTestClass(TestCase):

    def setUp(self):
        self.client = Client()
        self.dragon1 = self.create_default_dragon()
        self.dragon1.name = 'dragon1'
        self.dragon2 = self.create_default_dragon()
        self.dragon2.name = 'dragon2'

        self.user1 = User.objects.create_user(
            username='user1', 
            email='user1@example.com', 
            password='user1')
        self.user2 = User.objects.create_user(
            username='user2', 
            email='user2@example.com', 
            password='user2')

        self.player1 = self.default_player(self.user1)
        self.player2 = self.default_player(self.user2)

        self.dragon1.owner = self.user1
        self.dragon2.owner = self.user2

    def tearDown(self):
        self.dragon1.delete()
        self.dragon2.delete()
        self.user1.delete()
        self.user2.delete()
        self.player1.delete()
        self.player2.delete()

    def create_default_dragon(self):
        default_dragon = Dragon()
        default_dragon.attack = 100
        default_dragon.defense = 100
        default_dragon.speed = 100
        default_dragon.hp = 100
        default_dragon.save()
        return default_dragon

    def default_player(self, user):
        default_player = Player()
        default_player.user = user
        default_player.money = 100
        default_player.save()
        return default_player
    
    def test_damage_dragon1_attack_greater_than_dragon2_defense(self):
        damage_dragon1 = 100
        defense_dragon2 = 60
        expeceted_damage = damage_dragon1 - defense_dragon2
        taken_damage = damage(damage_dragon1, defense_dragon2)
        self.assertEqual(expeceted_damage, taken_damage)

    def test_damage_dragon1_attack_lesser_than_dragon2_defense(self):
        damage_dragon1 = 100
        defense_dragon2 = 110
        default_damage = 5
        taken_damage = damage(damage_dragon1, defense_dragon2)
        self.assertEqual(default_damage, taken_damage)

    def test_generate_stats(self):
        stat1 = 100
        stat2 = 100
        lower_bound = 0.4*(stat1 + stat2)
        upper_bound = 0.6*(stat1 + stat2)
        generated_stat = generate_stat(stat1, stat2)
        self.assertTrue( upper_bound > generated_stat > lower_bound)

    def test_stats_bound(self, stat1, stat2, generated_stat):
        lower_bound = 0.4*(stat1 + stat2)
        upper_bound = 0.6*(stat1 + stat2)
        return upper_bound >= generated_stat >= lower_bound

    def test_create_dragon(self):
        created_dragon = create_dragon(self.dragon1, self.dragon2)
        self.assertTrue(self.test_stats_bound(self.dragon1.attack, self.dragon2.attack, created_dragon.attack))
        self.assertTrue(self.test_stats_bound(self.dragon1.defense, self.dragon2.defense, created_dragon.defense))
        self.assertTrue(self.test_stats_bound(self.dragon1.speed, self.dragon2.speed, created_dragon.speed))
        self.assertTrue(self.test_stats_bound(self.dragon1.hp, self.dragon2.hp, created_dragon.hp))
        self.assertEqual(created_dragon.for_sale, False)
        self.assertEqual(created_dragon.price, 0)
    
    def test_start_fight(self):
        fight_result = start_fight(self.dragon1, self.dragon2)
        self.assertTrue(fight_result.dragon_winner_name)
        self.assertTrue(fight_result.dragon_winner_owner)
        self.assertTrue(fight_result.dragon_loser_name)
        self.assertTrue(fight_result.dragon_loser_owner)
        self.assertTrue(fight_result.rounds)

    def test_transfer_stolen_money(self):
        stolen_amount = transfer_stolen_money(self.user1, self.user2)
        EXPECETED_STOLEN_AMOUNT = 5
        self.assertEqual(EXPECETED_STOLEN_AMOUNT, stolen_amount)

    def test_validate_if_dragons_can_fight_with_two_different_owners(self):
        result = validate_if_dragons_can_fight(self.user1, self.dragon1, self.dragon2)
        self.assertEqual(result, True)
    
    def test_validate_if_dragons_can_fight_with_same_user(self):
        self.dragon2.owner = self.user1
        result = validate_if_dragons_can_fight(self.user1, self.dragon1, self.dragon2)
        self.assertEqual(result, False)

    def test_index_view__client_not_logged(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 302)
    
    def test_index_view_client_logged(self):
        self.client.login(username='user1',password='user1')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_my_sale_view__client_not_logged(self):
        response = self.client.get('/my_sale')
        self.assertEqual(response.status_code, 302)
    
    def test_my_sale_view_client_logged(self):
        self.client.login(username='user1',password='user1')
        response = self.client.get('/my_sale')
        self.assertEqual(response.status_code, 200)    

    def test_remove_from_market_with_valid_id(self):
        self.client.login(username='user1',password='user1')
        response = self.client.post('/remove_from_market/1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "updated")


    







    