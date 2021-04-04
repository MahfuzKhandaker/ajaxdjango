from django import forms
from pagedown.widgets import AdminPagedownWidget
from ajaxify.models import Post


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=AdminPagedownWidget())
    class Meta:
        model = Post
        fields = ['title', 'slug', 'summary', 'description', 'main_image', 'categories', 'likes', 'is_featured']

