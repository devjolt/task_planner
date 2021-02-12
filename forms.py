from django import forms
from django.forms import ModelForm
from .models import ItemModel

class ItemForm(ModelForm):
    class Meta:
        model = ItemModel
        fields = ('item',)