from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse

from .models import UploadHistory, Equipment
from .serializers import UploadHistorySerializer, EquipmentSerializer, UserSerializer
from .services import process_csv_file, generate_pdf_report

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [] 
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            history_record = process_csv_file(file_obj, request.user)
            serializer = UploadHistorySerializer(history_record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
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
    permission_classes = [IsAuthenticated]
    serializer_class = UploadHistorySerializer

    def get_queryset(self):
        return UploadHistory.objects.filter(user=self.request.user).order_by('-uploaded_at')[:5]

class PDFReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        latest = UploadHistory.objects.filter(user=request.user).order_by('-uploaded_at').first()
        if not latest:
            return Response({"error": "No data found"}, status=404)
            
        pdf_buffer = generate_pdf_report(latest.id)
        
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{latest.id}.pdf"'
        return response