from django.contrib import admin
from .models import Recipe, Ingredient, RecipeStep, Favourite

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'prep_duration_minutes', 'cook_duration_minutes', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    list_filter = ('created_by', 'created_at')
    inlines = [IngredientInline, RecipeStepInline]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipe', 'quantity')
    search_fields = ('name', 'recipe__title')

@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'order', 'description')
    search_fields = ('recipe__title',)
    ordering = ('recipe', 'order')

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created_at')
    search_fields = ('user__username', 'recipe__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

