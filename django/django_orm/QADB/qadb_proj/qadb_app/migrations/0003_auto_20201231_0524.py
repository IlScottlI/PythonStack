# Generated by Django 3.1.4 on 2020-12-31 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qadb_app', '0002_auto_20201231_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='complete_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
