from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pet_category(models.Model):
    name = models.TextField()
    image = models.FileField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Pets(models.Model):
    pet_id = models.TextField()
    pet_name = models.TextField()
    gender = models.TextField()
    age = models.TextField()
    adoption_fee = models.IntegerField()
    img = models.FileField()
    dis = models.TextField()
    category=models.ForeignKey(Pet_category,on_delete=models.CASCADE,related_name="pets")



    