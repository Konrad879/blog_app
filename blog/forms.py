from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    body = forms.CharField(
        required=True, 
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Enter your Blog Post",
                "class": "form-control"
            }
            ), 
            label="",

        )
    
    class Meta:
        model = BlogPost
        exclude = ("user",)
