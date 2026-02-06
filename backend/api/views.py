from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db.models import Count
from django.http import HttpResponse
from .services import generate_pdf_report
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .models import UploadHistory, Equipment
from .serializers import UploadHistorySerializer, EquipmentSerializer
from .services import process_csv_file, generate_pdf_report

class FileUploadView(APIView):
    """
    API View to handle CSV file uploads.
    """
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Pass request.user to the service
            history_record = process_csv_file(file_obj, request.user)
            serializer = UploadHistorySerializer(history_record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Returns data for the most recent upload to populate the main dashboard.
    Includes: Summary Stats, Type Distribution (for Charts), and Table Data.
    """
    def get(self, request, *args, **kwargs):
        # Filter by User
        latest_upload = UploadHistory.objects.filter(user=request.user).order_by('-uploaded_at').first()
        
        if not latest_upload:
            return Response({"message": "No data available"}, status=status.HTTP_204_NO_CONTENT)

        summary_serializer = UploadHistorySerializer(latest_upload)
        equipment_qs = latest_upload.equipments.all()
        equipment_serializer = EquipmentSerializer(equipment_qs, many=True)
        type_distribution = equipment_qs.values('type').annotate(count=Count('type'))

        return Response({
            "summary": summary_serializer.data,
            "distribution": type_distribution,
            "equipment_list": equipment_serializer.data
        })

class HistoryListView(generics.ListAPIView):
    """
    Returns the last 5 uploaded datasets.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UploadHistorySerializer

    def get_queryset(self):
        # Return only current user's history
        return UploadHistory.objects.filter(user=self.request.user).order_by('-uploaded_at')[:5]


class PDFReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Filter by User to prevent accessing others' reports
        latest = UploadHistory.objects.filter(user=request.user).order_by('-uploaded_at').first()
        if not latest:
            return Response({"error": "No data found"}, status=404)
            
        pdf_buffer = generate_pdf_report(latest.id)
        if not pdf_buffer:
             return Response({"error": "Report generation failed"}, status=500)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{latest.id}.pdf"'
        return response
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [] 
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)