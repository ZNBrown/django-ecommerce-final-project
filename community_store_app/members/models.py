from django.db import models
from django.contrib.auth.models import User
from communities.models import Community


ROLE_CHOICES =(
    ("Admin","admin"),
    ("Member", "member")
)


# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

#TODO: change user model to deal with emails for logging in primarily
#or at least return email right
    def __str__(self):
        return f'{self.user.email}'

class Membership(models.Model):
    user_id = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    community_id = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True)
    member_role = models.CharField(max_length=50, choices=ROLE_CHOICES)


    def __str__(self):
        return f'{self.user_id.user.email}'