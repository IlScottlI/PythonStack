# Generated by Django 3.1.4 on 2020-12-24 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dt_planner_app', '0007_track_calendar_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='calendar_dt',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='calendar_history', to='dt_planner_app.calendar'),
            preserve_default=False,
        ),
    ]
