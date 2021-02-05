from django.urls import path
from . import views

#todo/
urlpatterns = [
    path('', views.multi_category_todo, name='multi_category_todo'),
    #path('', views.home, name='home'),
    path('kill_all', views.kill_all, name='kill_all'),
]