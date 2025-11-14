from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeStep

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'picture', 'quantity']

class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['id', 'order', 'description', 'image']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    steps = RecipeStepSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description',
            'prep_duration_minutes', 'cook_duration_minutes',
            'thumbnail', 'ingredients', 'steps',
            'created_by', 'created_at'
        ]
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        steps_data = validated_data.pop('steps', [])

        recipe = Recipe.objects.create(**validated_data)

        # Save Ingredients
        for ing in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ing)

        # Save Steps (SAFE handling of `order`)
        for step in steps_data:
            order = step.pop("order")  # remove order from dict
            RecipeStep.objects.create(recipe=recipe, order=order, **step)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        steps_data = validated_data.pop('steps', [])

        # Update main recipe fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.prep_duration_minutes = validated_data.get('prep_duration_minutes', instance.prep_duration_minutes)
        instance.cook_duration_minutes = validated_data.get('cook_duration_minutes', instance.cook_duration_minutes)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)
        instance.save()

        # --- INGREDIENTS ---
        # Clear old ingredients and recreate new ones
        instance.ingredients.all().delete()
        for ing in ingredients_data:
            Ingredient.objects.create(recipe=instance, **ing)

        # --- STEPS ---
        # Clear old steps and recreate new steps with safe handling of 'order'
        instance.steps.all().delete()
        for step in steps_data:
            order = step.pop("order")  # remove order to avoid duplicate
            RecipeStep.objects.create(recipe=instance, order=order, **step)

        return instance
