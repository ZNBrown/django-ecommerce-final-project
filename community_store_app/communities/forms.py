from django import forms
from .models import Community

class CreateCommunityForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(max_length=50)

    class Meta:
        model = Community
        fields = ['name', 'description', 'location']