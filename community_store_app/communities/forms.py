from django import forms
from .models import Community, Product

class CreateCommunityForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(max_length=50)

    class Meta:
        model = Community
        fields = ['name', 'description', 'location']

class AddProductForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.FloatField()
    image = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'user_id', 'community_id']
        widgets = {'user_id': forms.HiddenInput(), 'community_id': forms.HiddenInput()}
