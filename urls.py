from django.urls import path
from . import views

#todo/
urlpatterns = [
    path('', views.home, name='home'),
]