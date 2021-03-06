# Generated by Django 3.1.4 on 2020-12-31 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qadb_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qadb',
            name='actions',
        ),
        migrations.AddField(
            model_name='qadb',
            name='actions',
            field=models.ManyToManyField(blank=True, related_name='actions_qadb', to='qadb_app.Action'),
        ),
        migrations.RemoveField(
            model_name='qadb',
            name='additional_detail',
        ),
        migrations.AddField(
            model_name='qadb',
            name='additional_detail',
            field=models.ManyToManyField(blank=True, related_name='additional_detail_qadb', to='qadb_app.AdditionalDetail'),
        ),
    ]
