from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name='home'),
    path('discover/', views.discover, name='discover'),
    path('discovery/', views.discovery, name='discovery'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    # ... other routes ...
]