from django.urls import path
from .views import ExceptionQueueView, RuleBuilderView, ManualMatchView, BulkActionView

app_name = 'reconciliation'

urlpatterns = [
    path('exceptions/', ExceptionQueueView.as_view(), name='exception_queue'),
    path('rule-builder/', RuleBuilderView.as_view(), name='rule_builder'),
    path('manual-match/<int:transaction_id>/', ManualMatchView.as_view(), name='manual_match'),
    path('bulk-action/', BulkActionView.as_view(), name='bulk_action'),
]
