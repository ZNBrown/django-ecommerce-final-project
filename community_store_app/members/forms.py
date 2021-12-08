from django import forms
from .models import Member
from communities.models import Membership, Request
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class JoinCommunityForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['user_id', 'community_id', 'reason']
        widgets = {'user_id': forms.HiddenInput(), 'reason': forms.Textarea}

    def __init__(self, *args, **kwargs):
        super(JoinCommunityForm, self).__init__(*args, **kwargs)
        self.fields['community_id'].label = "Community Name"
