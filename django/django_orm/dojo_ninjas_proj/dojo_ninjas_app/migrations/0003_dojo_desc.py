# Generated by Django 3.1.4 on 2020-12-12 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_ninjas_app', '0002_auto_20201212_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='dojo',
            name='desc',
            field=models.TextField(null=True),
        ),
    ]
