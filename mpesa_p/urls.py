from django.urls import path

from mpesa_p import views


app_name = "mpesa_p"

urlpatterns = [
    path('', views.home, name="home"),
    path('token', views.token, name='token'),
    path('pay', views.pay, name='pay'),
    path('stk', views.stk, name="stk")

]
