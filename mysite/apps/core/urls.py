
from django.urls import path
from . import views

app_name = 'core' # Registering the namespace

urlpatterns = [
    path('', views.splash, name='splash'),
    path('landing/', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('features/', views.features, name='features'),
    path('pricing/', views.pricing, name='pricing'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
]
