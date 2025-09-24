from django.urls import path
from .views import lipa_na_mpesa_view, mpesa_callback_view, pay

app_name = 'mpesa_p'

urlpatterns = [
    path('pay/', pay, name='pay'),
    path('lipa_na_mpesa/', lipa_na_mpesa_view, name='lipa_na_mpesa'),
    path('mpesa_callback/', mpesa_callback_view, name='mpesa_callback'),
]
