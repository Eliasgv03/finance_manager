# tags/forms.py
from django import forms
from .models import Tag

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'tag_type', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Tag Name'}),
            'tag_type': forms.Select(attrs={'class': 'tag-type-select'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }