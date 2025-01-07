from django.db import models


# Create your models here.
class Character(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    character_image = models.CharField(max_length=2000)
    
    def __str__(self):
        return self.name
