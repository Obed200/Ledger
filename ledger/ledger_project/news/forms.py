from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "dek", "category", "image", "body"]
        widgets = {
            "dek": forms.Textarea(attrs={"rows": 2}),
            "body": forms.Textarea(attrs={"rows": 12}),
        }
