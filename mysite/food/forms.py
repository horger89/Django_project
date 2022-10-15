
from django import forms
from .models import item ,Comment

class ItemForm(forms.ModelForm):
    class Meta():
        model = item
        fields = ['item_name','item_disc','item_price','item_image']

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ['text']



