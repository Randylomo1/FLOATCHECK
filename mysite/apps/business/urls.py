from django.urls import path
from . import views

urlpatterns = [
    path('setup/', views.business_setup, name='business_setup'),
]
