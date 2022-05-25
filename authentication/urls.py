from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = "authentication"
urlpatterns = [
    path('login/', auth_views.auth_login, name="login"),
    path('signup/', views.signup, name="login"),
]