from django.urls import path
from . import views

urlpatterns = [
    # Example endpoints
    path('recipes/', views.RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', views.RecipeRetrieveUpdateDeleteView.as_view(), name='recipe-detail'),
    path("recipes/<int:id>/delete/", views.RecipeDeleteView.as_view(), name="recipe-delete"),
    path("recipes/bulk-upload/", views.BulkUploadRecipeView.as_view(), name="recipe-bulk-upload"),
    path('recipes/<int:pk>/download/', views.RecipePDFDownloadView.as_view(), name='recipe-pdf-download'),
    path('recipes/<int:pk>/favourite/', views.FavouriteRecipeView.as_view(), name='recipe-favourite'),
]   