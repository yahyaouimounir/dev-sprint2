from django.db import models
import uuid 
from django.contrib.auth.models import User

# Create your models here 

    
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    is_admin= models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Event(models.Model):
    title = models.CharField(primary_key=True,max_length=100, unique=True)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    responsible_person = models.CharField(max_length=100)
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    )
    status= models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming') 
    type = models.CharField(max_length=50)
    duration = models.IntegerField()
    participants = models.ManyToManyField(Member, blank=True,related_name='events_participated') 
    def __str__(self): 
        return self.title 
    
    
class requete(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True) 
    participant = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='requetes_made')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name='event_requetes')
    status = models.BooleanField(default=False) 
    notification = models.OneToOneField('Notification', on_delete=models.CASCADE, null=True, blank=True,related_name='requete_notification')
    def __str__(self):
        return f"requete from {self.participant.username} for {self.event.title}"
    
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True) 
    requete = models.OneToOneField(requete, on_delete=models.CASCADE, null=True, blank=True, related_name='notification_requete')
    status = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"Notification for {self.Member.username} about {self.event.title}" 