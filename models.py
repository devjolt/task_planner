from django.db import models

# Create your models here.
#class ListModel (models.Model):
#    todo_list = models.CharField()

class ItemModel (models.Model):
    #todo_list = models.ForeignKey(ListModel, on_delete=models.CASCADE)
    item = models.CharField(max_length = 30)