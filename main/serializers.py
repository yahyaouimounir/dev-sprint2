from .models import Member, Event, requete, Notification 
from rest_framework import serializers 
from django.contrib.auth import get_user_model


User = get_user_model() 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)  # Assurez-vous que user est required
    
    class Meta:
        model = Member
        fields = ['user', 'is_admin']
    
    def create(self, validated_data):
        # Vérifiez d'abord si 'user' existe dans validated_data
        if 'user' not in validated_data:
            raise serializers.ValidationError({"user": "This field is required."})
            
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        member = Member.objects.create(user=user, **validated_data)
        return member  
    
    def validate (self, data): 
        email = data.get("email")
        username = data.get("username")
        password = data.get('password')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})
        return data
       
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.save()
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.save()
        return instance 
    
class EventSerializer(serializers.ModelSerializer):
    participants = MemberSerializer(many=True, read_only=True)  
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'responsible_person', 'status', 'type', 'duration', 'participants']  
    
    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        return event  
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.location = validated_data.get('location', instance.location)
        instance.responsible_person = validated_data.get('responsible_person', instance.responsible_person)
        instance.status = validated_data.get('status', instance.status)
        instance.type = validated_data.get('type', instance.type)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.save()
        return instance 
    
    def validate (self, data): 
        title = data.get("title")
        description = data.get("description")
        date = data.get("date")

        if Event.objects.filter(title=title).exists():
            raise serializers.ValidationError({"title": "An event with this title already exists."})

        if Event.objects.filter(description=description).exists():
            raise serializers.ValidationError({"description": "This description is already taken."})

        if Event.objects.filter(date=date).exists():
            raise serializers.ValidationError({"date": "This date is already registered."}) 
        return data 
    
class requeteSerializer(serializers.ModelSerializer):
    participant = MemberSerializer(read_only=True)  
    event = EventSerializer(read_only=True)  
    
    class Meta:
        model = requete
        fields = ['id', 'participant', 'event', 'status']  
    
    def create(self, validated_data):
        Requete = requete.objects.create(**validated_data)
        return Requete  
    
    def update(self, instance, validated_data):
        instance.participant = validated_data.get('participant', instance.participant)
        instance.event = validated_data.get('event', instance.event)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
     
    def validate(self, data):
        participant = data.get("participant")
        event = data.get("event")
        if requete.objects.filter(participant=participant, event=event).exists():
            raise serializers.ValidationError({"participant": "This participant has already made a request for this event."})
        return data
    
