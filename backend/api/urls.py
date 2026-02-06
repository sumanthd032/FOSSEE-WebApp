from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 
from .views import FileUploadView, DashboardDataView, HistoryListView, PDFReportView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'), 
    
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('dashboard/', DashboardDataView.as_view(), name='dashboard-data'),
    path('history/', HistoryListView.as_view(), name='history-list'),
    path('report/pdf/', PDFReportView.as_view(), name='pdf-report'),
]