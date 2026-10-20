from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Follow, Post, PostLike

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
        post = Post.objects.create(
            title=f"generic{i}", description="new post", user=user, status="active"
        )
        posts.append(post)

    return posts


class FollowModelTests(TestCase):

    def test_quantity_followers(self):
        """
        quantity_followers() return the quantity of followers you have
        with some followings
        """
        users, influencers = create_generic_users_influencers(
            users_quantity=3, influencers_quantity=1
        )
        Follow.objects.create(followed_user=influencers[0], following_user=users[0])
        Follow.objects.create(followed_user=influencers[0], following_user=users[1])
        Follow.objects.create(followed_user=influencers[0], following_user=users[2])
        self.assertEqual(influencers[0].quantity_followings, 0)
        self.assertEqual(influencers[0].quantity_followers, 3)

    def test_quantity_followings(self):
        """
        quantity_followings() return the quantity of followings you have
        """
        users, influencers = create_generic_users_influencers(
            users_quantity=1, influencers_quantity=3
        )
        Follow.objects.create(followed_user=influencers[0], following_user=users[0])
        Follow.objects.create(followed_user=influencers[1], following_user=users[0])
        Follow.objects.create(followed_user=influencers[2], following_user=users[0])
        self.assertEqual(users[0].quantity_followers, 0)
        self.assertEqual(users[0].quantity_followings, 3)


class FollowViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="seguidor")
        self.author = User.objects.create_user(username="autor")
        self.url = reverse("facebook:follow-user", args=[self.author.pk])
        self.client.force_login(self.user)

    def test_ajax_follow_toggles_following_state(self):
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "is_following": True})
        self.assertTrue(
            Follow.objects.filter(
                followed_user=self.author, following_user=self.user
            ).exists()
        )

        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "is_following": False})
        self.assertFalse(
            Follow.objects.filter(
                followed_user=self.author, following_user=self.user
            ).exists()
        )

    def test_post_follow_link_reflects_following_state(self):
        Post.objects.create(
            user=self.author,
            title="Publicación de prueba",
            description="Contenido de prueba",
            status="active",
        )
        response = self.client.get(reverse("facebook:index"))

        self.assertContains(
            response,
            'class="text-decoration-none js-follow-toggle text-primary"',
        )
        self.assertContains(response, ">Seguir</a>")

        Follow.objects.create(followed_user=self.author, following_user=self.user)
        response = self.client.get(reverse("facebook:index"))

        self.assertContains(
            response,
            'class="text-decoration-none js-follow-toggle text-danger"',
        )
        self.assertContains(response, ">Dejar de seguir</a>")


class PostLikeButtonTemplateTests(TestCase):

    def test_post_card_and_modal_like_buttons_share_post_identity(self):
        user = User.objects.create_user(username="lector")
        post = Post.objects.create(
            user=User.objects.create_user(username="autor"),
            title="Publicación de prueba",
            description="Contenido de prueba",
            status="active",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("facebook:index"))

        self.assertEqual(
            response.content.count(f'data-post-id="{post.pk}"'.encode()), 2
        )
        self.assertEqual(response.content.count(b"btn-like-inner-post"), 2)


class PostLikeModelTests(TestCase):

    def test_quantity_postlikes(self):
        """
        quantity_postlikes() should return the quantity of likes a user did in a many posts
        """
        users, influencers = create_generic_users_influencers(
            users_quantity=1, influencers_quantity=3
        )
        posts = create_generic_posts(influencers[0], posts_quantity=5)

        PostLike.objects.create(
            liked_post=posts[0], user_like=users[0], reaction="like"
        )
        PostLike.objects.create(
            liked_post=posts[1], user_like=users[0], reaction="love"
        )
        PostLike.objects.create(
            liked_post=posts[2], user_like=users[0], reaction="dislike"
        )
        PostLike.objects.create(
            liked_post=posts[3], user_like=users[0], reaction="love"
        )

        PostLike.objects.create(
            liked_post=posts[0], user_like=influencers[1], reaction="like"
        )
        PostLike.objects.create(
            liked_post=posts[1], user_like=influencers[1], reaction="love"
        )

        self.assertEqual(users[0].quantity_postlikes, 4)
        self.assertEqual(influencers[1].quantity_postlikes, 2)

    def test_quantity_likes(self):
        """
        quantity_likes() should return the quantity of likes a post have
        """
        users, influencers = create_generic_users_influencers(
            users_quantity=1, influencers_quantity=5
        )
        posts = create_generic_posts(users[0], posts_quantity=2)

        PostLike.objects.create(
            liked_post=posts[0], user_like=influencers[0], reaction="like"
        )
        PostLike.objects.create(
            liked_post=posts[0], user_like=influencers[1], reaction="love"
        )
        PostLike.objects.create(
            liked_post=posts[0], user_like=influencers[2], reaction="love"
        )
        PostLike.objects.create(
            liked_post=posts[0], user_like=influencers[3], reaction="love"
        )
        PostLike.objects.create(
            liked_post=posts[0], user_like=influencers[4], reaction="love"
        )

        PostLike.objects.create(
            liked_post=posts[1], user_like=influencers[0], reaction="love"
        )
        PostLike.objects.create(
            liked_post=posts[1], user_like=influencers[1], reaction="love"
        )
        PostLike.objects.create(
            liked_post=posts[1], user_like=influencers[2], reaction="love"
        )

        self.assertEqual(posts[0].quantity_likes, 5)
        self.assertEqual(posts[1].quantity_likes, 3)

    def test_user_cannot_like_same_post_twice(self):
        """
        A user only can like a post only one time and no more
        """
        users, influencers = create_generic_users_influencers(
            users_quantity=1, influencers_quantity=1
        )
        posts = create_generic_posts(influencers[0], posts_quantity=1)

        PostLike.objects.create(
            liked_post=posts[0],
            user_like=users[0],
            reaction="like",
        )

        with self.assertRaises(IntegrityError):
            PostLike.objects.create(
                liked_post=posts[0],
                user_like=users[0],
                reaction="love",
            )


class PostCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="juan", password="123456")

    def test_authenticated_user_can_access_create_post(self):
        """
        Si el usuario esta logueado podra ingresar a la vista para crear un post
        """
        self.client.login(username="juan", password="123456")

        response = self.client.get(reverse("facebook:create-post"))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_access_create_post(self):
        """
        Si el usuario no esta logueado no tendra acceso para crear un post
        """
        response = self.client.get(reverse("facebook:create-post"))
        self.assertEqual(response.status_code, 302)


class CommentCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="comentador")
        self.post = Post.objects.create(
            user=User.objects.create_user(username="autor"),
            title="Publicación de prueba",
            description="Contenido de prueba",
            status="active",
        )
        self.url = reverse("facebook:create-comment", args=[self.post.pk])

    def test_authenticated_user_can_create_comment(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"comment": "Buen post"})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["comments_count"], 1)
        self.assertIn("Buen post", response.json()["comment_html"])
        self.assertEqual(self.post.comments.get().user, self.user)

    def test_authenticated_user_can_create_comment_with_image(self):
        self.client.force_login(self.user)
        image = SimpleUploadedFile(
            "comment.jpg", b"image-content", content_type="image/jpeg"
        )

        with (
            TemporaryDirectory() as media_root,
            override_settings(MEDIA_ROOT=media_root),
        ):
            response = self.client.post(
                self.url, {"comment": "Buen post", "image": image}
            )

            comment = self.post.comments.get()
            self.assertEqual(response.status_code, 201)
            self.assertTrue(comment.image)
            self.assertIn(comment.image.url, response.json()["comment_html"])

    def test_empty_comment_is_rejected(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"comment": "   "})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.post.comments.count(), 0)

    def test_anonymous_user_cannot_create_comment(self):
        response = self.client.post(self.url, {"comment": "Buen post"})

        self.assertEqual(response.status_code, 302)
