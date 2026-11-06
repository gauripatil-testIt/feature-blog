from django.utils import timezone
from django.views import generic

from .forms import NewsletterSubscribeForm
from .models import NewsletterSubscriber, Post


def published_posts():
    return Post.objects.filter(is_published=True, published_at__lte=timezone.now())


SUBSCRIPTION_SUCCESS_NOTICE = "Thanks for subscribing!"
ALREADY_SUBSCRIBED_NOTICE = "You're already subscribed"


class PostListView(generic.ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return published_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = NewsletterSubscribeForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = NewsletterSubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if NewsletterSubscriber.objects.filter(email__iexact=email).exists():
                notice = ALREADY_SUBSCRIBED_NOTICE
            else:
                NewsletterSubscriber.objects.create(email=email)
                notice = SUBSCRIPTION_SUCCESS_NOTICE
            context = self.get_context_data(form=NewsletterSubscribeForm(), notice=notice)
            return self.render_to_response(context)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return published_posts()
