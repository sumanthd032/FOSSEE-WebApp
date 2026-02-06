import pandas as pd
from .models import UploadHistory, Equipment
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def process_csv_file(file_obj):
    """
    Parses CSV, calculates stats, and saves to DB using Pandas.
    """
    try:
        # Read CSV using Pandas
        df = pd.read_csv(file_obj)
        
        # Standardize column names 
        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
        
        # Calculate Statistics
        stats = {
            'total_records': len(df),
            'avg_flowrate': df['flowrate'].mean(),
            'avg_pressure': df['pressure'].mean(),
            'avg_temperature': df['temperature'].mean(),
        }
        
        # Create History Record
        history = UploadHistory.objects.create(
            file_name=file_obj.name,
            **stats
        )
        
        # Bulk Create Equipment Records
        equipment_instances = [
            Equipment(
                upload=history,
                equipment_id=row.get('equipment_id', f"EQ-{i}"),
                name=row.get('equipment_name', 'Unknown'),
                type=row.get('type', 'Generic'),
                flowrate=row.get('flowrate', 0.0),
                pressure=row.get('pressure', 0.0),
                temperature=row.get('temperature', 0.0)
            )
            for i, row in df.iterrows()
        ]
        
        Equipment.objects.bulk_create(equipment_instances)
        
        return history
        
    except Exception as e:
        raise ValueError(f"Error processing CSV: {str(e)}")
    
def generate_pdf_report(history_id):
    """Generates a PDF buffer for the given upload history."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Fetch Data
    try:
        history = UploadHistory.objects.get(id=history_id)
        equipments = history.equipments.all()
    except UploadHistory.DoesNotExist:
        return None

    # Title
    elements.append(Paragraph(f"Chemical Equipment Report: {history.file_name}", styles['Title']))
    elements.append(Paragraph(f"Date: {history.uploaded_at.strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Summary Section
    summary_data = [
        ["Metric", "Value"],
        ["Total Records", str(history.total_records)],
        ["Avg Flowrate", f"{history.avg_flowrate:.2f}"],
        ["Avg Pressure", f"{history.avg_pressure:.2f}"],
        ["Avg Temperature", f"{history.avg_temperature:.2f}"]
    ]
    t_summary = Table(summary_data, colWidths=[200, 200])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t_summary)
    elements.append(Spacer(1, 20))

    # Detailed Table (First 50 records to save space)
    elements.append(Paragraph("Equipment Data (First 50 Records)", styles['Heading2']))
    
    data = [["ID", "Name", "Type", "Pressure"]]
    for eq in equipments[:50]:
        data.append([eq.equipment_id, eq.name, eq.type, str(eq.pressure)])

    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t)

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer