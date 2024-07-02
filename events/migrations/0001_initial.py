# Generated by Django 5.0.6 on 2024-07-01 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='speakers/photos/')),
                ('documents', models.FileField(blank=True, null=True, upload_to='speakers/documents/')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='sponsors/logos/')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('event_type', models.CharField(choices=[('Conference', 'Conference'), ('Workshop', 'Workshop'), ('Webinar', 'Webinar'), ('Concert', 'Concert'), ('Corporate', 'Corporate Event')], max_length=50)),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
                ('total_tickets', models.PositiveIntegerField()),
                ('ticket_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vip_tickets', models.PositiveIntegerField(default=0)),
                ('vip_ticket_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('speakers', models.ManyToManyField(related_name='events', to='events.speaker')),
                ('sponsors', models.ManyToManyField(related_name='events', to='events.sponsor')),
            ],
        ),
    ]
