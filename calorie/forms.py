from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Product, Profile


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SelectProductForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('food_selected', 'quantity',)

    def __init__(self, user, *args, **kwargs):
        super(SelectProductForm, self).__init__(*args, **kwargs)
        self.fields['food_selected'].queryset = Product.objects.filter(person_of=user)


class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'quantity', 'calorie', 'fat', 'protein', 'carbohydrate')