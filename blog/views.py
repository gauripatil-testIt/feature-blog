from django.utils import timezone
from django.views import generic

from .models import Post


def published_posts():
    return Post.objects.filter(is_published=True, published_at__lte=timezone.now())


class PostListView(generic.ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return published_posts()


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return published_posts()
