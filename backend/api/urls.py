from django.urls import path
from .views import FileUploadView, DashboardDataView, HistoryListView, PDFReportView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('dashboard/', DashboardDataView.as_view(), name='dashboard-data'),
    path('history/', HistoryListView.as_view(), name='history-list'),
    path('report/pdf/', PDFReportView.as_view(), name='pdf-report'),
]