from django import forms
from .models import Member, Membership
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class JoinCommunityForm(forms.ModelForm):
    community_name = forms.CharField(max_length=50)
    reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Membership
        fields = ['community_name', 'reason']
