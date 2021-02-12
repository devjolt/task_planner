from django.urls import path
from . import views

#todo/
urlpatterns = [
    #path('', views.todo_model, name='todo_model'),
    #path('addTodoItem/', views.addTodoView), 
    #path('deleteTodoItem/<int:i>/', views.deleteTodoView), 

    path('', views.multi_category_todo, name='multi_category_todo'),
    #path('', views.home, name='home'),
    
    
    path('kill_all', views.kill_all, name='kill_all'),
]