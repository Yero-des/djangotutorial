from django.test import TestCase
from .models import User, Follow

# Create your tests here.
class FollowModelTests(TestCase):
    
    def test_quantity_followers(self):
        """
        quantity_followers() return the quantity of followers you have
        with some followings
        """
        influencer = User.objects.create(username="top", role='staff')
        user1 = User.objects.create(username="user1", role='user')
        user2 = User.objects.create(username="user2", role='user')
        user3 = User.objects.create(username="user3", role='user')
        Follow.objects.create(followed_user=influencer, following_user=user1)
        Follow.objects.create(followed_user=influencer, following_user=user2)
        Follow.objects.create(followed_user=influencer, following_user=user3)
        self.assertEqual(influencer.quantity_followings, 0)
        self.assertEqual(influencer.quantity_followers, 3)
        
    def test_quantity_followings(self):
        """
        quantity_followings() return the quantity of followings you have done
        """
        user = User.objects.create(username="random", role="user")
        influencer1 = User.objects.create(username="top1", role='staff')
        influencer2 = User.objects.create(username="top2", role='staff')
        influencer3 = User.objects.create(username="top3", role='staff')
        Follow.objects.create(followed_user=influencer1, following_user=user)
        Follow.objects.create(followed_user=influencer2, following_user=user)
        Follow.objects.create(followed_user=influencer3, following_user=user)
        self.assertEqual(user.quantity_followers, 0)
        self.assertEqual(user.quantity_followings, 3)