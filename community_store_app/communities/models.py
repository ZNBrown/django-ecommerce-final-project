from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    community_id = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


    

