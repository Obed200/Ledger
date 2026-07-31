from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Article(models.Model):
    CATEGORY_CHOICES = [
        ("Business", "Business"),
        ("Markets", "Markets"),
        ("Leadership", "Leadership"),
        ("Technology", "Technology"),
        ("Money", "Money"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    dek = models.CharField(max_length=300, help_text="One-sentence summary shown on listings.")
    body = models.TextField(help_text="Leave a blank line between paragraphs.")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Business")
    image = models.ImageField(upload_to="articles/%Y/%m/", blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200] or "story"
            slug = base
            n = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news:article_detail", args=[self.slug])

    @property
    def paragraphs(self):
        return [p.strip() for p in self.body.split("\n") if p.strip()]
