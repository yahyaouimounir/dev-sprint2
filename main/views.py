from django.shortcuts import render
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view , permission_classes
from .models import Event, requete, Member, Notification
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import MemberSerializer, EventSerializer, UserSerializer, requeteSerializer
user = get_user_model() 
from django.shortcuts import get_object_or_404
from .acceptmail import sendMail
from .refuseMail import sendRefuseMail 
import csv
from datetime import datetime
from django.http import JsonResponse
#===========================register===========================#
@api_view(['POST']) 
def register(request): 
    member_ser = MemberSerializer(data=request.data)
    if member_ser.is_valid():
        member = member_ser.save()
        refresh = RefreshToken.for_user(member.user) 
        return Response({
            "message": "Member created successfully",
            "member": member_ser.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED) 
    return Response(member_ser.errors, status=status.HTTP_400_BAD_REQUEST) 

#===========================login===========================#
@csrf_exempt
@api_view(['POST']) 
def login(request): 
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password=password)
    
    if user :
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#===========================logout===========================#
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data['refresh']
    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklist the refresh token
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except :
        return Response({'error': 'something happened'}, status=status.HTTP_400_BAD_REQUEST) 
    
#===========================upgrade to admin===========================#
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Décommentez cette ligne
def upgrade_to_admin(request, id):
    # Vérifie que l'utilisateur est authentifié
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, 
                      status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Vérifie que l'utilisateur actuel est admin
        if not request.user.member.is_admin:
            return Response({'error': 'Admin privileges required'}, 
                          status=status.HTTP_403_FORBIDDEN)
            
        # Récupère le membre à promouvoir
        member_to_upgrade = get_object_or_404(Member, id=id)
        member_to_upgrade.is_admin = True
        member_to_upgrade.save()
        
        return Response({'message': 'User upgraded to admin'}, 
                       status=status.HTTP_200_OK)
        
    except AttributeError:
        return Response({'error': 'User profile not found'},
                      status=status.HTTP_400_BAD_REQUEST)

#===========================create event===========================#
@api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
def create_event(request): 
    if not request.user.member.is_admin:
        return Response({'error': 'Admin privileges required'}, status=status.HTTP_403_FORBIDDEN)
    else:
        event_ser = EventSerializer(data=request.data)
        if event_ser.is_valid():
            event = event_ser.save()
            return Response({
                "message": "Event created successfully",
                "event": event_ser.data
            }, status=status.HTTP_201_CREATED) 
        return Response(event_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    

#===========================update event===========================#
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request, title):
    if not request.user.member.is_admin:
        return Response({'error': 'Admin privileges required'}, status=status.HTTP_403_FORBIDDEN)
    
    event = get_object_or_404(Event, title=title)
    event_ser = EventSerializer(event, data=request.data, partial=True)
    
    if event_ser.is_valid():
        event_ser.save()
        return Response({
            "message": "Event updated successfully",
            "event": event_ser.data
        }, status=status.HTTP_200_OK) 
    
    return Response(event_ser.errors, status=status.HTTP_400_BAD_REQUEST)


#===========================delete event===========================#
@api_view(['DELETE']) 
@permission_classes([IsAuthenticated]) 
def delete_event(request, title): 
    if not request.user.member.is_admin:
        return Response({'error': 'Admin privileges required'}, status=status.HTTP_403_FORBIDDEN)
    
    event = get_object_or_404(Event, title=title)
    event.delete()
    return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#===========================view all events===========================#
@api_view(['GET']) 
def view_events(request): 
    events = Event.objects.all() 
    serializer = EventSerializer(events, many=True) 
    return Response(serializer.data, status=status.HTTP_200_OK)

#===========================view event according to the title===========================#

@api_view(['GET']) 
def view_event(request, title): 
    event = get_object_or_404(Event, title=title) 
    serializer = EventSerializer(event) 
    
    return Response(serializer.data, status=status.HTTP_200_OK)


#===========================view requetes for admin===========================#
@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def view_requetes_admin(request): 
    if not request.user.member.is_admin:
        return Response({'error': 'Admin privileges required'}, status=status.HTTP_403_FORBIDDEN)
    
    requetes = requete.objects.all() 
    serializer = requeteSerializer(requetes, many=True) 

    return Response(serializer.data, status=status.HTTP_200_OK) 


#===========================send requete===========================#
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_requete(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        event = get_object_or_404(Event, title=request.data.get('event_title'))
        requete_ser = requeteSerializer(data=request.data)
        
        if requete_ser.is_valid():
            requete = requete_ser.save(event=event, participant=request.user.member)
            notification = send_notification(requete)  
            return Response({
                "message": "Requete sent successfully",
                "requete": requete_ser.data,
                "notification": {
                    "id": notification.id,
                    "status": notification.status,
                    "date_creation": notification.date_creation
                }
            }, status=status.HTTP_201_CREATED) 
        
        return Response(requete_ser.errors, status=status.HTTP_400_BAD_REQUEST)

#===========================view requetes for member===========================#

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_requetes_member(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    Requetes = requete.objects.filter(participant=request.user.member) 
    serializer = requeteSerializer(Requetes, many=True) 

    return Response(serializer.data, status=status.HTTP_200_OK)


#===========================send notification===========================#
def send_notification(requete):
    notification = Notification.objects.create(requete=requete, status=False)
    requete.notification = notification
    requete.save()
    return notification

#===========================mark notification as read===========================#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, id):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    notification = get_object_or_404(Notification, id=id)
    if notification.status == False:
        notification.status = True
        notification.save()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)


#


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mark_notification_as_unread(request, id):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    notification = get_object_or_404(Notification, id=id)
    if (notification.status == True):
         notification.status = False
         notification.save()
         return Response({"message": "Notification marked as unread"}, status=status.HTTP_200_OK)
    


#===========================view notifications===========================#

@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def view_notifications(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    elif not request.user.member.is_admin:
        return Response({'error': 'Admin privileges required'}, status=status.HTTP_403_FORBIDDEN)
    else :
        notifications = Notification.objects.filter(status=False) 
        for notif in notifications:
            notif.status = True
            notif.save()
       
        serializer = requeteSerializer(notifications, many=True) 
    return Response(serializer.data, status=status.HTTP_200_OK)


#===========================accept requete===========================#

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def accept_requete(request, id):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    elif not request.user.member.is_admin:
        return Response({'error': 'Admin privileges required'}, status=status.HTTP_403_FORBIDDEN)
    else:
        Requete = get_object_or_404(requete, id=id) 
        Requete.status = "accepted"
        Requete.save()
        unique_id = str(Requete.id)+str(Requete.participant.id)
        sendMail(
            user=Requete.participant.user.username,
            id_user=unique_id,
            event_name=Requete.event.title,
            email=Requete.participant.user.email
        )
        return Response({"message": "Requete accepted successfully"}, status=status.HTTP_200_OK)



#===========================refuse requete===========================#

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def refuse_requete(request, id):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    elif not request.user.member.is_admin:
        return Response({'error': 'Admin privileges required'}, status=status.HTTP_403_FORBIDDEN)
    else:
        Requete = get_object_or_404(requete, id=id) 
        unique_id = str(Requete.id)+str(Requete.participant.id)
        Requete.status = "refused"
        sendRefuseMail(
            user=Requete.participant.user.username,
            event_name=Requete.event.title,
            email=Requete.participant.user.email
        )
        return Response({"message": "Requete Refused successfully"}, status=status.HTTP_200_OK)


#===========================display participation status===========================#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_participation_status(request, event_title):
    # Get the requete(s) for current user and specified event
    requetes = requete.objects.filter(
        event__title=event_title,          
        participant=request.user.member           
    ).values('status')                     
    return Response(
        {'statuses': list(requetes)},      
        status=status.HTTP_200_OK
    )


#===========================import events===========================#
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_events(request):
    if not request.user.member.is_admin:
        return JsonResponse({'error': 'Admin privileges required'}, status=403)
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        results = {
            'created': 0,
            'errors': [],
            'skipped': 0
        }
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            required_columns = {'title', 'description', 'date', 'location', 
                               'responsible_person', 'status', 'type', 'duration'}
            
            if not required_columns.issubset(reader.fieldnames):
                return JsonResponse({'error': 'Missing required columns'}, status=400)

            for row_num, row in enumerate(reader, start=2):  
                try:
                    if Event.objects.filter(title=row['title']).exists():    # checking if the event already exists
                        results['skipped'] += 1
                        continue
                    # Clean and validate data
                    status = row['status'].lower()
                    if status == 'cancelled':  
                        status = 'canceled'
                        
                    Event.objects.create(
                        title=row['title'],
                        description=row['description'],
                        date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                        location=row['location'],
                        responsible_person=row['responsible_person'],
                        status=status,
                        type=row['type'],
                        duration=int(row['duration'])
                    )
                    results['created'] += 1
                except Exception as e:
                    results['errors'].append({
                        'row': row_num,
                        'error': str(e),
                        'data': row
                    })
                except Event.DoesNotExist:
                    results['skipped'] += 1

            return JsonResponse({
                'message': f'Successfully imported {results["created"]} events',
                'errors': results['errors'],
                'skipped': results['skipped']
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'No CSV file uploaded'}, status=400)