from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductsPageView.as_view(), name="productos")
]