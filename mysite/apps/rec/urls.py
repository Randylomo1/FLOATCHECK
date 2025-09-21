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
]
