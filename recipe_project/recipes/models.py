from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    prep_duration_minutes = models.PositiveIntegerField(default=0)
    cook_duration_minutes = models.PositiveIntegerField(default=0)
    thumbnail = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=100, blank=True)
    picture = models.URLField(blank=True, null=True)


    def __str__(self):
        return f"{self.name} ({self.recipe.title})"


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    description = models.TextField()
    image = models.URLField(blank=True, null=True)


    class Meta:
        ordering = ['order']


    def __str__(self):
        return f"Step {self.order} for {self.recipe.title}"

class Favourite(models.Model):
    user = models.ForeignKey(User, related_name='favourites', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='favourited_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'recipe')


    def __str__(self):
        return f"{self.user} favourited {self.recipe}"