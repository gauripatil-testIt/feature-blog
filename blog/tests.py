from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post


class BlogViewsTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title="Hello Multi-Repo",
            slug="hello-multi-repo",
            body="Features live in their own repositories.",
            is_published=True,
            published_at=timezone.now() - timedelta(minutes=1),
        )

    def test_list_shows_published_post(self):
        response = self.client.get(reverse("blog:index"))
        self.assertContains(response, "Hello Multi-Repo")

    def test_list_hides_draft(self):
        Post.objects.create(title="Draft", slug="draft", body="...", is_published=False)
        response = self.client.get(reverse("blog:index"))
        self.assertNotContains(response, "Draft")

    def test_detail_renders_published_post(self):
        response = self.client.get(reverse("blog:detail", args=(self.post.slug,)))
        self.assertContains(response, "Features live in their own repositories.")

    def test_detail_404_for_draft(self):
        draft = Post.objects.create(title="Draft", slug="draft", body="...", is_published=False)
        response = self.client.get(reverse("blog:detail", args=(draft.slug,)))
        self.assertEqual(response.status_code, 404)
