from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
from django import forms


def home_page(request):
    events = Event.objects.filter(start_date_time__gte=timezone.now()).order_by('start_date_time')
    return render(request, 'home_page.html', {'events': events})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username in ['rishi', 'ayan'] and password == '1234':
            user = authenticate(request, username=username, password=password)
            if user is None:
                user = User.objects.create_user(username=username, password=password, is_staff=True, is_superuser=True)
            login(request, user)
            return redirect('admin_page')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'admin_login.html')

@login_required
def admin_page(request):
    return render(request, 'admin_page.html')

@login_required
def add_event(request):
    if request.method == 'POST':
        event_types = Event.EVENT_TYPES

        name = request.POST['name']
        event_type = request.POST['event_type']
        start_date = request.POST['start_date_time']
        start_time = request.POST['start_time']
        end_date = request.POST['end_date_time']
        end_time = request.POST['end_time']
        total_tickets = request.POST['total_tickets']
        ticket_price = request.POST['ticket_price']
        vip_tickets = request.POST['vip_tickets']
        vip_ticket_price = request.POST['vip_ticket_price']
        
        start_date_time = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        end_date_time = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")

        event = Event.objects.create(
            name=name,
            event_type=event_type,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            total_tickets=total_tickets,
            ticket_price=ticket_price,
            vip_tickets=vip_tickets,
            vip_ticket_price=vip_ticket_price
        )

        speaker_id = request.POST.get('speakers')
        sponsor_id = request.POST.get('sponsors')

        if speaker_id:
            event.speaker = Speaker.objects.get(id=speaker_id)

        if sponsor_id:
            event.sponsor = Sponsor.objects.get(id=sponsor_id)

        event.save()
        messages.success(request, 'Event added successfully')
        return redirect('admin_page')

    speakers = Speaker.objects.all()
    sponsors = Sponsor.objects.all()
    event_types = Event.EVENT_TYPES
    return render(request, 'add_event.html', {'speakers': speakers, 'sponsors': sponsors, 'event_types': event_types})

@login_required
def admin_events(request):
    events = Event.objects.all().order_by('start_date_time')
    return render(request, 'admin_events.html', {'events': events})

# @login_required
# def edit_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     if request.method == 'POST':
#         event.name = request.POST.get('name')
#         event.event_type = request.POST.get('event_type')
#         event.start_date_time = request.POST.get('start_date_time')
#         event.end_date_time = request.POST.get('end_date_time')
#         event.total_tickets = request.POST.get('total_tickets')
#         event.available_tickets = request.POST.get('available_tickets')
#         event.save()
#         messages.success(request, 'Event updated successfully.')
#         return redirect('admin_events')
#     return render(request, 'edit_event.html', {'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, 'Event deleted successfully.')
    return redirect('admin_events')

def admin_logout(request):
    logout(request)
    return redirect('home_page')

def events_by_type(request, event_type):
    events = Event.objects.filter(event_type=event_type)
    return render(request, 'event_list.html', {'events': events, 'event_type': event_type})

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

def event_list(request, event_type):
    events = Event.objects.filter(event_type=event_type)
    return render(request, 'event_list.html', {'events': events, 'event_type': event_type})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Event

from django.shortcuts import render, get_object_or_404, redirect

def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        # Handle form submission and then redirect to home page
        return redirect('home_page')
    return render(request, 'event_details.html', {'event': event})



def register_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            ticket_type = request.POST.get('ticket_type')

            if ticket_type == 'normal' and event.available_normal_tickets > 0:
                event.available_normal_tickets -= 1
                event.add_registered_user(name, email, 'normal')
            elif ticket_type == 'vip' and event.available_vip_tickets > 0:
                event.available_vip_tickets -= 1
                event.add_registered_user(name, email, 'vip')
            else:
                messages.error(request, 'Selected ticket type is not available.')
                return redirect('event_details', event_id=event.id)

            event.save()
            messages.success(request, 'You have successfully registered for the event.')
            return redirect('home_page')
    else:
        form = RegistrationForm()

    return render(request, 'register_ticket.html', {'event': event, 'form': form})

def speaker_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        bio = request.POST['bio']
        photo = request.FILES.get('image', None)
        documents = request.FILES.get('file', None)

        # Create Speaker object
        speaker = Speaker.objects.create(
            name=name,
            bio=bio,
            photo=photo,
            documents=documents
        )

        # Optionally, you can add validation or error handling here

        messages.success(request, 'Speaker registered successfully.')
        return redirect('home_page')

    return render(request, 'speaker_register.html')

def sponsor_registration(request):
    return render(request, 'sponsor_register.html')

def show_speakers(request):
    speakers = Speaker.objects.all()
    return render(request, 'show_speakers.html', {'speakers': speakers})