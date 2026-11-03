# feature-blog

Installable Django app that provides the blog feature. This is its own git
repository and is consumed by `project-core`.

## Install

Local development (from the project repo):

```bash
pip install -e ../feature-blog
```

Production (pinned git tag):

```bash
pip install "django-feature-blog @ git+https://github.com/your-org/feature-blog.git@v0.1.0"
```

## Wire into a Django project

```python
INSTALLED_APPS += ["blog"]

urlpatterns += [path("blog/", include("blog.urls"))]
```

Migrations live in this repo (`blog/migrations/`) and are applied by the
project that installs the app.

## Test

Run from `project-core` after installing this package:

```bash
python manage.py test blog
```
