import csv
from datetime import datetime
from .models import Event  

def import_events_from_csv(file_path):
    results = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            csv_reader = csv.DictReader(f)
            
            for row in csv_reader:
                results['total'] += 1
                
                try:
                    # Nettoyer et formater les données
                    status = row['status'].lower()
                    if status == 'upcoming':
                        status = 'upcoming'
                    elif status == 'cancelled' or status == 'canceled':
                        status = 'canceled'
                    else:
                        status = 'completed'
                    
                    # Convertir la date du format string à l'objet date
                    event_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                    
                    # Créer ou mettre à jour l'événement
                    event, created = Event.objects.update_or_create(
                        title=row['title'],
                        defaults={
                            'description': row['description'],
                            'date': event_date,
                            'location': row['location'],
                            'responsible_person': row['responsible_person'],
                            'status': status,
                            'type': row['type'],
                            'duration': int(row['duration'])
                        }
                    )
                    
                    results['success'] += 1
                    
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append({
                        'row': row,
                        'error': str(e)
                    })
                    continue
                    
    except Exception as e:
        results['errors'].append({
            'error': f"Erreur lors de la lecture du fichier: {str(e)}"
        })
    
    return results