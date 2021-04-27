from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class CoffeeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CoffeeUser.objects.create(user=instance, credits=2)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.coffeeuser.save()

class CoffeeRecipe(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    coffee = models.IntegerField()
    milk = models.IntegerField()
    #water = models.IntegerField()
    chocolate = models.IntegerField()
    cost = models.IntegerField()


class CoffeeOrder(models.Model):
    user = models.ForeignKey(CoffeeUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(CoffeeRecipe, on_delete=models.CASCADE)
    time = models.DateTimeField()