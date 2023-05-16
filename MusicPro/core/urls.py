from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('webpay-plus/commit', webpay_plus_commit, name="webpay_plus_commit")
]