from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import json

from apps.blog.models import Post, Like


class UserTestCase(TestCase):
    PASSWORD = "strongpass1"

    def setUp(self):
        author_user = get_user_model().objects.create(
            username="author", email="author@mial.com"
        )
        author_user.set_password(self.PASSWORD)
        author_user.save()

        client = APIClient()
        response = client.post(
            "/api/token/",
            {"username": "author", "password": self.PASSWORD},
            format="json",
        )
        self.author_user_token = json.loads(response.content)["token"]

        liked_user = get_user_model().objects.create(
            username="liked_user", email="liked_user@mial.com"
        )
        liked_user.set_password(self.PASSWORD)
        liked_user.save()

        client = APIClient()
        response = client.post(
            "/api/token/",
            {"username": "liked_user", "password": self.PASSWORD},
            format="json",
        )
        self.liked_user_token = json.loads(response.content)["token"]

        unliked_user = get_user_model().objects.create(
            username="unliked_user", email="unliked_user@mial.com"
        )
        unliked_user.set_password(self.PASSWORD)
        unliked_user.save()

        client = APIClient()
        response = client.post(
            "/api/token/",
            {"username": "unliked_user", "password": self.PASSWORD},
            format="json",
        )
        self.unliked_user_token = json.loads(response.content)["token"]

        self.publish_post = Post.objects.create(
            title="Publish post title",
            description="Text description",
            user=author_user,
            publish=True,
        )

        self.unpublish_post = Post.objects.create(
            title="Unpublish post title",
            description="Text description",
            user=author_user,
            publish=False,
        )

        Like.objects.create(post=self.publish_post, user=liked_user, like=True)
        Like.objects.create(post=self.publish_post, user=unliked_user, like=False)

    def test_get_publish_post(self):
        client = APIClient()

        response = client.get("/api/posts/{}/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["title"], "Publish post title")

    def test_get_unpublish_post(self):
        client = APIClient()

        response = client.get("/api/posts/{}/".format(self.unpublish_post.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_unpublish_post_as_owner(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + self.author_user_token)

        response = client.get("/api/posts/{}/".format(self.unpublish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + self.liked_user_token)

        response = client.post(
            "/api/posts/", {"title": "Create post", "description": "Post description."}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_as_anonim(self):
        client = APIClient()

        response = client.post(
            "/api/posts/", {"title": "Create post", "description": "Post description."}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_like_as_anonim(self):
        client = APIClient()

        response = client.get("/api/posts/{}/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["is_liked"], None)

    def test_get_post_with_like(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + self.liked_user_token)

        response = client.get("/api/posts/{}/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["is_liked"], True)

    def test_get_post_with_unlike(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + self.unliked_user_token)

        response = client.get("/api/posts/{}/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["is_liked"], False)

    def test_get_post_with_not_liked_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + self.author_user_token)

        response = client.get("/api/posts/{}/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["is_liked"], None)

    def test_create_like(self):
        user = get_user_model().objects.create(
            username="test_like_user", email="test_like_user@mial.com"
        )
        user.set_password(self.PASSWORD)
        user.save()

        like = Like.objects.filter(user=user, post=self.publish_post).first()
        self.assertIsNone(like)

        client = APIClient()
        response = client.post(
            "/api/token/",
            {"username": "test_like_user", "password": self.PASSWORD},
            format="json",
        )
        token = json.loads(response.content)["token"]

        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        response = client.post("/api/posts/{}/like/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        like = Like.objects.filter(user=user, post=self.publish_post).first()
        self.assertIsInstance(like, Like)
        self.assertTrue(like.like)

    def test_create_unlike(self):
        user = get_user_model().objects.create(
            username="test_unlike_user", email="test_unlike_user@mial.com"
        )
        user.set_password(self.PASSWORD)
        user.save()

        like = Like.objects.filter(user=user, post=self.publish_post).first()
        self.assertIsNone(like)

        client = APIClient()
        response = client.post(
            "/api/token/",
            {"username": "test_unlike_user", "password": self.PASSWORD},
            format="json",
        )
        token = json.loads(response.content)["token"]

        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        response = client.post("/api/posts/{}/unlike/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        like = Like.objects.filter(user=user, post=self.publish_post).first()
        self.assertIsInstance(like, Like)
        self.assertFalse(like.like)

    def test_delete_reaction(self):
        user = get_user_model().objects.create(
            username="delete_reaction_user", email="delete_reaction_user@mial.com"
        )
        user.set_password(self.PASSWORD)
        user.save()

        Like.objects.create(user=user, post=self.publish_post, like=True)

        client = APIClient()
        response = client.post(
            "/api/token/",
            {"username": "delete_reaction_user", "password": self.PASSWORD},
            format="json",
        )
        token = json.loads(response.content)["token"]

        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        response = client.post(
            "/api/posts/{}/delete_reaction/".format(self.publish_post.id)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        like = Like.objects.filter(user=user, post=self.publish_post).first()
        self.assertIsNone(like)

    def test_update_like(self):
        user = get_user_model().objects.get(username="unliked_user")
        like = Like.objects.filter(user=user, post=self.publish_post).first()
        self.assertIsInstance(like, Like)
        self.assertFalse(like.like)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + self.unliked_user_token)

        response = client.post("/api/posts/{}/like/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        like = Like.objects.filter(user=user, post=self.publish_post).first()
        self.assertIsInstance(like, Like)
        self.assertTrue(like.like)

    def test_update_unlike(self):
        user = get_user_model().objects.get(username="liked_user")
        like = Like.objects.filter(user=user, post=self.publish_post).first()
        self.assertIsInstance(like, Like)
        self.assertTrue(like.like)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + self.liked_user_token)

        response = client.post("/api/posts/{}/unlike/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        like = Like.objects.filter(user=user, post=self.publish_post).first()
        self.assertIsInstance(like, Like)
        self.assertFalse(like.like)
