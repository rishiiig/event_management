from django.db import models
import json

class Speaker(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='speakers/photos/', blank=True, null=True)
    documents = models.FileField(upload_to='speakers/documents/', blank=True, null=True)

    def __str__(self):
        return self.name

class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='sponsors/logos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_TYPES = [
        ('Conference', 'Conference'),
        ('Workshop', 'Workshop'),
        ('Webinar', 'Webinar'),
        ('Concert', 'Concert'),
        ('Corporate', 'Corporate Event'),
    ]

    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    total_tickets = models.PositiveIntegerField()
    normal_ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_normal_tickets = models.PositiveIntegerField(default=0)
    available_vip_tickets = models.PositiveIntegerField(default=0)
    vip_ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    speaker = models.ForeignKey(Speaker, on_delete=models.SET_NULL, null=True, blank=True)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True, blank=True)
    registered_users = models.TextField(default='[]')  # To store JSON data

    def __str__(self):
        return self.name

    def add_registered_user(self, name, email, ticket_type):
        users = json.loads(self.registered_users)
        users.append({'name': name, 'email': email, 'ticket_type': ticket_type})
        self.registered_users = json.dumps(users)
        self.save()
