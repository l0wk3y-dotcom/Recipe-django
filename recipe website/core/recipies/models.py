from django.db import models
from django.db.models import Model
from django.template.defaultfilters import length
from django.contrib.auth.models import User


# Create your models here.

class Recipe(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    recipe_name=models.CharField(max_length=50)
    recipe_description=models.TextField()
    image=models.ImageField(upload_to="recipe_images")

    def __str__(self):
        return self.recipe_name