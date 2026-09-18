from django.test import TestCase
from .models import Follow, Post, Like
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

def create_generic_users_influencers(users_quantity, influencers_quantity):
    
    users = []
    influencers = []
    
    for i in range(users_quantity):
        user = User.objects.create(username=f"user{i}")
        users.append(user)
        
    for i in range(influencers_quantity):
        influencer = User.objects.create(username=f"influencer{i}")
        influencers.append(influencer)
        
    return users, influencers

def create_generic_posts(user, posts_quantity):
    
    posts = []
    
    for i in range(posts_quantity):
        post = Post.objects.create(title=f"generic{i}", body="new post", user=user, status="active")
        posts.append(post)
        
    return posts
    
class FollowModelTests(TestCase):
    
    def test_quantity_followers(self):
        """
        quantity_followers() return the quantity of followers you have
        with some followings
        """
        users, influencers = create_generic_users_influencers(users_quantity=3, influencers_quantity=1)
        Follow.objects.create(followed_user=influencers[0], following_user=users[0])
        Follow.objects.create(followed_user=influencers[0], following_user=users[1])
        Follow.objects.create(followed_user=influencers[0], following_user=users[2])
        self.assertEqual(influencers[0].quantity_followings, 0)
        self.assertEqual(influencers[0].quantity_followers, 3)
        
    def test_quantity_followings(self):
        """
        quantity_followings() return the quantity of followings you have
        """
        users, influencers = create_generic_users_influencers(users_quantity=1, influencers_quantity=3)
        Follow.objects.create(followed_user=influencers[0], following_user=users[0])
        Follow.objects.create(followed_user=influencers[1], following_user=users[0])
        Follow.objects.create(followed_user=influencers[2], following_user=users[0])
        self.assertEqual(users[0].quantity_followers, 0)
        self.assertEqual(users[0].quantity_followings, 3)
        
class LikeModelTests(TestCase):
        
    def test_quantity_user_likes(self):
        """
        quantity_user_likes() should return the quantity of likes a user did in a many posts
        """
        users, influencers = create_generic_users_influencers(users_quantity=1, influencers_quantity=3)
        posts = create_generic_posts(influencers[0], posts_quantity=5)
        
        Like.objects.create(liked_post=posts[0], user_like=users[0], reaction="like")
        Like.objects.create(liked_post=posts[1], user_like=users[0], reaction="love")
        Like.objects.create(liked_post=posts[2], user_like=users[0], reaction="dislike")
        Like.objects.create(liked_post=posts[3], user_like=users[0], reaction="love")
        
        Like.objects.create(liked_post=posts[0], user_like=influencers[1], reaction="like")
        Like.objects.create(liked_post=posts[1], user_like=influencers[1], reaction="love")
        
        self.assertEqual(users[0].quantity_user_likes, 4)
        self.assertEqual(influencers[1].quantity_user_likes, 2)
        
    def test_quantity_likes(self):
        """
        quantity_likes() should return the quantity of likes a post have
        """
        users, influencers = create_generic_users_influencers(users_quantity=1, influencers_quantity=5)
        posts = create_generic_posts(users[0], posts_quantity=2)
        
        Like.objects.create(liked_post=posts[0], user_like=influencers[0], reaction="like")
        Like.objects.create(liked_post=posts[0], user_like=influencers[1], reaction="love")
        Like.objects.create(liked_post=posts[0], user_like=influencers[2], reaction="love")
        Like.objects.create(liked_post=posts[0], user_like=influencers[3], reaction="love")
        Like.objects.create(liked_post=posts[0], user_like=influencers[4], reaction="love")
        
        Like.objects.create(liked_post=posts[1], user_like=influencers[0], reaction="love")
        Like.objects.create(liked_post=posts[1], user_like=influencers[1], reaction="love")
        Like.objects.create(liked_post=posts[1], user_like=influencers[2], reaction="love")
        
        self.assertEqual(posts[0].quantity_likes, 5)
        self.assertEqual(posts[1].quantity_likes, 3)
        
    def test_user_cannot_like_same_post_twice(self):
        """
        A user only can like a post only one time and no more
        """
        users, influencers = create_generic_users_influencers(users_quantity=1,influencers_quantity=1)
        posts = create_generic_posts(influencers[0],posts_quantity=1)

        Like.objects.create(
            liked_post=posts[0],
            user_like=users[0],
            reaction="like",
        )

        with self.assertRaises(IntegrityError):
            Like.objects.create(
                liked_post=posts[0],
                user_like=users[0],
                reaction="love",
            )

class PostCreateViewTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='juan',
            password='123456'
        )

    def test_authenticated_user_can_access_create_post(self):
        """
        Si el usuario esta logueado podra ingresar a la vista para crear un post
        """
        self.client.login(
            username='juan',
            password='123456'
        )

        response = self.client.get(reverse('facebook:create-post'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_access_create_post(self):
        """
        Si el usuario no esta logueado no tendra acceso para crear un post
        """
        response = self.client.get(reverse('facebook:create-post'))
        self.assertEqual(response.status_code, 302)