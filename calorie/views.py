from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView
from .forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import Category, Product, Profile, ProfileFood

# Create your views here.
class Register(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    queryset = Category.objects.all()
