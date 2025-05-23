# Generated by Django 5.2 on 2025-04-19 02:17

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_member_is_participant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='request',
        ),
        migrations.RemoveField(
            model_name='member',
            name='is_participant',
        ),
        migrations.CreateModel(
            name='requete',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('status', models.BooleanField(default=False)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_requetes', to='main.event')),
                ('notification', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requete_notification', to='main.notification')),
                ('participant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requetes_made', to='main.member')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='requete',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_requete', to='main.requete'),
        ),
        migrations.DeleteModel(
            name='Request',
        ),
    ]
