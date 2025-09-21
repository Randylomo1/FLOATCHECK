from rest_framework import serializers
from .models import SubscriptionPlan, PaymentLink, BusinessSubscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class PaymentLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLink
        fields = '__all__'
        read_only_fields = ('business', 'payment_link_id', 'is_active')

class BusinessSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessSubscription
        fields = '__all__'
        read_only_fields = ('business',)
