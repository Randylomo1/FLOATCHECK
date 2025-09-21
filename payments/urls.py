from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api

router = DefaultRouter()
router.register(r'subscription-plans', api.SubscriptionPlanViewSet)
router.register(r'payment-links', api.PaymentLinkViewSet)
router.register(r'business-subscriptions', api.BusinessSubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
