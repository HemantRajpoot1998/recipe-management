from openpyxl import load_workbook
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Ingredient, Recipe, Favourite, RecipeStep
from .serializers import RecipeSerializer
from .permissions import IsCreator, IsViewer
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from rest_framework.parsers import MultiPartParser, FormParser
from reportlab.lib.pagesizes import A4


# Creator: CRUD
class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            print(self.request.user, "current user")
            return [permissions.IsAuthenticated(), IsCreator()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RecipeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsCreator()]
        return [permissions.AllowAny()]


class RecipeDeleteView(generics.DestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = "id"

    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsCreator()]


# Creator: Bulk Upload
class BulkUploadRecipeView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCreator]

    def post(self, request):
        excel_file = request.FILES.get("file")

        if not excel_file:
            return Response({"error": "Excel file is required."}, status=400)

        # Save file temporarily
        file_path = f"/tmp/{excel_file.name}"
        with open(file_path, "wb+") as f:
            for chunk in excel_file.chunks():
                f.write(chunk)

        # Call Celery task
        from .tasks import process_bulk_recipe_upload
        process_bulk_recipe_upload.delay(file_path, request.user.id)

        return Response({
            "message": "Bulk upload started. Processing in background.",
            "status": "PENDING"
        }, status=200)



# Viewer: Favourite
class FavouriteRecipeView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsViewer]

    def post(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        fav, created = Favourite.objects.get_or_create(user=request.user, recipe=recipe)
        if not created:
            fav.delete()
            return Response({'message': 'Removed from favourites'})
        return Response({'message': 'Added to favourites'})


# Viewer: PDF Download
class RecipePDFDownloadView(APIView):
    permission_classes = [permissions.AllowAny, IsViewer]

    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=404)

        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        y = 800

        # -------------------------
        # HEADER
        # -------------------------
        p.setFont("Helvetica-Bold", 16)
        p.drawString(60, y, f"Recipe: {recipe.title}")
        y -= 30

        p.setFont("Helvetica", 12)
        p.drawString(60, y, f"Description: {recipe.description}")
        y -= 30

        p.drawString(60, y, f"Prep Duration: {recipe.prep_duration_minutes} minutes")
        y -= 20

        p.drawString(60, y, f"Cook Duration: {recipe.cook_duration_minutes} minutes")
        y -= 40

        # -------------------------
        # INGREDIENTS SECTION
        # -------------------------
        p.setFont("Helvetica-Bold", 14)
        p.drawString(60, y, "Ingredients:")
        y -= 25

        p.setFont("Helvetica", 12)

        for ing in recipe.ingredients.all():
            if y <= 50:  # New page
                p.showPage()
                y = 800

            p.drawString(80, y, f"- {ing.name}")
            y -= 18

            # Handle picture field (string URL OR file)
            if ing.picture:
                picture_value = str(ing.picture)

                if picture_value.startswith("http"):
                    p.drawString(100, y, f"Image: {picture_value}")
                else:
                    p.drawString(100, y, f"Image: {request.build_absolute_uri(ing.picture.url)}")

                y -= 18

        y -= 20

        # -------------------------
        # STEPS SECTION
        # -------------------------
        p.setFont("Helvetica-Bold", 14)
        p.drawString(60, y, "Steps:")
        y -= 25

        p.setFont("Helvetica", 12)

        for step in recipe.steps.all():
            if y <= 70:
                p.showPage()
                y = 800

            p.drawString(80, y, f"Step {step.order}: {step.description}")
            y -= 18

            if step.image:
                image_val = str(step.image)

                if image_val.startswith("http"):
                    p.drawString(100, y, f"Image: {image_val}")
                else:
                    p.drawString(100, y, f"Image: {request.build_absolute_uri(step.image.url)}")

                y -= 18

            y -= 10

        # -------------------------
        # FINALIZE PDF
        # -------------------------
        p.showPage()
        p.save()

        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{recipe.title}.pdf"'

        return response