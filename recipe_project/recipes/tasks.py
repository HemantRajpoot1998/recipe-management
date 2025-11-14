from celery import shared_task
import openpyxl
from .models import Recipe, RecipeIngredient, RecipeStep
from django.contrib.auth.models import User

@shared_task
def process_bulk_recipe_upload(file_path, user_id):
    try:
        user = User.objects.get(id=user_id)
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            title, description, ingredient_data, step_data, prep, cook = row

            recipe = Recipe.objects.create(
                title=title,
                description=description,
                prep_duration_minutes=prep,
                cook_duration_minutes=cook,
                created_by=user
            )

            # INGREDIENTS
            ingredients = ingredient_data.split("|")
            for ing in ingredients:
                name, picture = ing.split("::")
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    name=name,
                    picture=picture
                )

            # STEPS
            steps = step_data.split("|")
            for step in steps:
                order, desc, image = step.split("::")
                RecipeStep.objects.create(
                    recipe=recipe,
                    order=int(order),
                    description=desc,
                    image=image
                )

        return "SUCCESS"

    except Exception as e:
        return str(e)
