from django.contrib import admin
from .models import (
    PaymentSource,
    Business,
    UserProfile,
    SubscriptionPlan,
    BusinessSubscription,
    PaymentLink,
)

admin.site.register(PaymentSource)
admin.site.register(Business)
admin.site.register(UserProfile)
admin.site.register(SubscriptionPlan)
admin.site.register(BusinessSubscription)
admin.site.register(PaymentLink)
