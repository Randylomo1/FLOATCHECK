from django.urls import path
from . import views

app_name = 'rec'

urlpatterns = [
    path('', views.reconciliation_list, name='reconciliation_list'),
    path('create/', views.create_reconciliation, name='create_reconciliation'),
    path('<int:reconciliation_id>/run/', views.run_reconciliation_view, name='run_reconciliation'),
    path('<int:reconciliation_id>/', views.reconciliation_detail, name='reconciliation_detail'),
    path('<int:reconciliation_id>/delete/', views.delete_reconciliation, name='delete_reconciliation'),
    path('<int:reconciliation_id>/upload/<str:record_type>/', views.upload_records, name='upload_records'),
    path('<int:reconciliation_id>/map/<str:record_type>/', views.map_columns, name='map_columns'),
    path('rules/', views.rule_builder, name='rule_builder'),
    path('rules/<int:rule_id>/delete/', views.delete_rule, name='delete_rule'),
    path('exceptions/', views.exception_queue, name='exception_queue'),
    path('<int:reconciliation_id>/report/', views.download_reconciliation_report, name='download_reconciliation_report'),
    path('<int:reconciliation_id>/schedule/', views.schedule_report, name='schedule_report'),
    path('scheduled_report/<int:report_id>/delete/', views.delete_scheduled_report, name='delete_scheduled_report'),
]
