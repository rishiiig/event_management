from django.contrib import admin
from .models import Event, Speaker, Sponsor

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'start_date_time', 'end_date_time', 'total_tickets', 'available_normal_tickets', 'available_vip_tickets', 'vip_ticket_price', 'speaker', 'sponsor')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'speaker':
            kwargs["queryset"] = Speaker.objects.all()
        elif db_field.name == 'sponsor':
            kwargs["queryset"] = Sponsor.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
