from django.db import models

# Create your models here.
class User(models.Model):
    _id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)
    panCard = models.CharField(max_length=10)
    aadharCard = models.CharField(max_length=12)

    def __str__(self):

        return self.name + "@" + self.email
        