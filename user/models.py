from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=10)
    userName=models.CharField(max_length=20,unique=True)
    dob=models.CharField(max_length=8)
    mobile = models.BigIntegerField()


    def __str__(self):
        return self.name