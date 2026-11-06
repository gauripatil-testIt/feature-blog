from datetime import timedelta
from html import unescape

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import NewsletterSubscriber, Post


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


class NewsletterSubscribeTests(TestCase):
    def test_index_shows_subscribe_form(self):
        response = self.client.get(reverse("blog:index"))
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'type="submit"')

    def test_valid_email_subscribes_and_shows_success(self):
        response = self.client.post(reverse("blog:index"), {"email": "reader@example.com"})
        self.assertTrue(NewsletterSubscriber.objects.filter(email="reader@example.com").exists())
        self.assertContains(response, "Thanks for subscribing!")

    def test_duplicate_email_shows_already_subscribed(self):
        NewsletterSubscriber.objects.create(email="reader@example.com")
        response = self.client.post(reverse("blog:index"), {"email": "Reader@Example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)
        self.assertIn("You're already subscribed", unescape(response.content.decode()))

    def test_empty_email_shows_inline_error(self):
        response = self.client.post(reverse("blog:index"), {"email": ""})
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)
        self.assertContains(response, "This field is required.")

    def test_invalid_email_shows_inline_error(self):
        response = self.client.post(reverse("blog:index"), {"email": "not-an-email"})
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)
        self.assertContains(response, "Enter a valid email address.")
