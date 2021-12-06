from django.db import models
from members.models import Member 

class Community(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=50)


    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    sold_status = models.BooleanField(default=False)
    image = models.FileField(upload_to=f"images/", null=True, verbose_name="")
    user_id = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, default=Member)
    community_id = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, default=Community)

    def __str__(self):
        return self.title

ROLE_CHOICES =(
    ("Admin","admin"),
    ("Member", "member")
)

class Membership(models.Model):
    user_id = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    community_id = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True)
    member_role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.user_id.user.email}'
    

