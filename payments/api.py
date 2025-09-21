from rest_framework import viewsets, serializers
from .models import SubscriptionPlan, PaymentLink, BusinessSubscription

# Serializers
class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class PaymentLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLink
        fields = '__all__'

class BusinessSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessSubscription
        fields = '__all__'

# ViewSets
class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

class PaymentLinkViewSet(viewsets.ModelViewSet):
    queryset = PaymentLink.objects.all()
    serializer_class = PaymentLinkSerializer

class BusinessSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = BusinessSubscription.objects.all()
    serializer_class = BusinessSubscriptionSerializer
