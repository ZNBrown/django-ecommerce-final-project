from django import forms
from .models import Community, Product

class CreateCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description', 'location']
        widgets = {'description': forms.Textarea}

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'user_id', 'community_id']
        widgets = {'user_id': forms.HiddenInput(), 'community_id': forms.HiddenInput(), 'description': forms.Textarea}