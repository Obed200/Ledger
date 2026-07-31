from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from accounts.views import is_admin_user

from .forms import ArticleForm
from .models import Article

CATEGORIES = [choice[0] for choice in Article.CATEGORY_CHOICES]


def home(request):
    category = request.GET.get("category")
    articles = Article.objects.select_related("author").all()
    if category in CATEGORIES:
        articles = articles.filter(category=category)

    featured = articles.filter(featured=True).first() or articles.first()
    rest = list(articles.exclude(pk=featured.pk)) if featured else []

    context = {
        "featured": featured,
        "side_stories": rest[:3],
        "grid_stories": rest[3:9],
        "categories": CATEGORIES,
        "active_category": category if category in CATEGORIES else "All",
        "authors": Profile.objects.select_related("user").filter(role="author"),
    }
    return render(request, "news/home.html", context)


def article_detail(request, slug):
    article = get_object_or_404(Article.objects.select_related("author", "author__profile"), slug=slug)
    return render(request, "news/article_detail.html", {"article": article})


@login_required
def author_dashboard(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Story published to The Ledger.")
            return redirect("news:author_dashboard")
    else:
        form = ArticleForm()

    mine = Article.objects.filter(author=request.user)
    return render(request, "news/author_dashboard.html", {"form": form, "articles": mine})


@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user and not is_admin_user(request.user):
        messages.error(request, "You can only delete your own stories.")
    else:
        article.delete()
        messages.success(request, "Story deleted.")
    return redirect(request.META.get("HTTP_REFERER") or "news:home")


@login_required
def toggle_featured(request, pk):
    if not is_admin_user(request.user):
        messages.error(request, "Only administrators can feature a story.")
        return redirect("news:home")
    article = get_object_or_404(Article, pk=pk)
    article.featured = not article.featured
    article.save()
    return redirect("accounts:admin_dashboard")
