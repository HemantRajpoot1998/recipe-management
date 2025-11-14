from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
     path('login/', views.UserLoginView.as_view(), name='user-login'),
     path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
]                                       
