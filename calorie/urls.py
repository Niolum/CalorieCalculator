from django.urls import path, include
from .views import (
    Register,
    CategoryListView
)


urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('register/', Register.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls'))
]