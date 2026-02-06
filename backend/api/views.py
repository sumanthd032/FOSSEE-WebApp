from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db.models import Count

from .models import UploadHistory, Equipment
from .serializers import UploadHistorySerializer, EquipmentSerializer
from .services import process_csv_file

class FileUploadView(APIView):
    """
    API View to handle CSV file uploads.
    """
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Delegate logic to the Service Layer (Step 1)
            history_record = process_csv_file(file_obj)
            serializer = UploadHistorySerializer(history_record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DashboardDataView(APIView):
    """
    Returns data for the most recent upload to populate the main dashboard.
    Includes: Summary Stats, Type Distribution (for Charts), and Table Data.
    """
    def get(self, request, *args, **kwargs):
        # Get the latest upload
        latest_upload = UploadHistory.objects.order_by('-uploaded_at').first()
        
        if not latest_upload:
            return Response({"message": "No data available"}, status=status.HTTP_204_NO_CONTENT)

        # 1. Summary Stats
        summary_serializer = UploadHistorySerializer(latest_upload)

        # 2. Equipment Data (Table)
        equipment_qs = latest_upload.equipments.all()
        equipment_serializer = EquipmentSerializer(equipment_qs, many=True)

        # 3. Type Distribution (For Charts) - Group by Type
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
    queryset = UploadHistory.objects.order_by('-uploaded_at')[:5]
    serializer_class = UploadHistorySerializer