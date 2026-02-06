import pandas as pd
from .models import UploadHistory, Equipment

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