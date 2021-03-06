# Generated by Django 3.1.4 on 2020-12-23 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Approver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('recurrenceRule', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approvers', models.ManyToManyField(blank=True, related_name='approver_calendar', to='dt_planner_app.Approver')),
                ('area', models.ManyToManyField(blank=True, related_name='area_calendar', to='dt_planner_app.Area')),
                ('business', models.ManyToManyField(blank=True, related_name='business_calendar', to='dt_planner_app.Business')),
            ],
        ),
        migrations.CreateModel(
            name='Locale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
                ('JSON_Data', models.JSONField(default=None)),
                ('date_picker', models.JSONField(default=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_locale', to='dt_planner_app.locale')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('required', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plant', models.ManyToManyField(blank=True, related_name='plant_question', to='dt_planner_app.Plant')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_status', to='dt_planner_app.plant')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=512)),
                ('password', models.CharField(max_length=255)),
                ('user_id', models.CharField(max_length=255)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='user/')),
                ('admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_plant', to='dt_planner_app.plant')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_plant', to='dt_planner_app.plant')),
                ('questions', models.ManyToManyField(blank=True, related_name='question_type', to='dt_planner_app.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_track', to='dt_planner_app.plant')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_track', to='dt_planner_app.status')),
                ('track_approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_approver', to='dt_planner_app.approver')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('calendar', models.ManyToManyField(related_name='response_calendar', to='dt_planner_app.Calendar')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='response_question', to='dt_planner_app.question')),
            ],
        ),
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_reason', to='dt_planner_app.plant')),
                ('questions', models.ManyToManyField(blank=True, related_name='question_reason', to='dt_planner_app.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('businesses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_module', to='dt_planner_app.business')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_module', to='dt_planner_app.plant')),
                ('questions', models.ManyToManyField(blank=True, related_name='question_module', to='dt_planner_app.Question')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_history', to='dt_planner_app.plant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_user', to='dt_planner_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module_department', to='dt_planner_app.module')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_department', to='dt_planner_app.plant')),
                ('questions', models.ManyToManyField(blank=True, related_name='question_department', to='dt_planner_app.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('area', models.ManyToManyField(blank=True, related_name='area_contributor', to='dt_planner_app.Area')),
                ('business', models.ManyToManyField(blank=True, related_name='business_contributor', to='dt_planner_app.Business')),
                ('department', models.ManyToManyField(blank=True, related_name='department_contributor', to='dt_planner_app.Department')),
                ('module', models.ManyToManyField(blank=True, related_name='module_contributor', to='dt_planner_app.Module')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_contributor', to='dt_planner_app.plant')),
                ('questions', models.ManyToManyField(blank=True, related_name='question_contributor', to='dt_planner_app.Question')),
                ('reasons', models.ManyToManyField(blank=True, related_name='reason_contributor', to='dt_planner_app.Reason')),
                ('types', models.ManyToManyField(blank=True, related_name='type_contributor', to='dt_planner_app.Type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_contributor', to='dt_planner_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('calendar_dt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar_comment', to='dt_planner_app.calendar')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_comment', to='dt_planner_app.area')),
            ],
        ),
        migrations.AddField(
            model_name='calendar',
            name='contributors',
            field=models.ManyToManyField(blank=True, related_name='contributor_calendar', to='dt_planner_app.Contributor'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_dt_creator', to='dt_planner_app.user'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='department',
            field=models.ManyToManyField(blank=True, related_name='department_calendar', to='dt_planner_app.Department'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='module',
            field=models.ManyToManyField(blank=True, related_name='module_calendar', to='dt_planner_app.Module'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_dt_owner', to='dt_planner_app.user'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_calendar', to='dt_planner_app.plant'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='question_calendar', to='dt_planner_app.Question'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='reasons',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reason_calendar', to='dt_planner_app.reason'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar_status', to='dt_planner_app.status'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='types',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_calendar', to='dt_planner_app.type'),
        ),
        migrations.AddField(
            model_name='business',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_business', to='dt_planner_app.plant'),
        ),
        migrations.AddField(
            model_name='business',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='question_business', to='dt_planner_app.Question'),
        ),
        migrations.AddField(
            model_name='area',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_area', to='dt_planner_app.department'),
        ),
        migrations.AddField(
            model_name='area',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_area', to='dt_planner_app.plant'),
        ),
        migrations.AddField(
            model_name='area',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='question_area', to='dt_planner_app.Question'),
        ),
        migrations.AddField(
            model_name='approver',
            name='area',
            field=models.ManyToManyField(blank=True, related_name='area_approver', to='dt_planner_app.Area'),
        ),
        migrations.AddField(
            model_name='approver',
            name='business',
            field=models.ManyToManyField(blank=True, related_name='business_approver', to='dt_planner_app.Business'),
        ),
        migrations.AddField(
            model_name='approver',
            name='department',
            field=models.ManyToManyField(blank=True, related_name='department_approver', to='dt_planner_app.Department'),
        ),
        migrations.AddField(
            model_name='approver',
            name='module',
            field=models.ManyToManyField(blank=True, related_name='module_approver', to='dt_planner_app.Module'),
        ),
        migrations.AddField(
            model_name='approver',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_approver', to='dt_planner_app.plant'),
        ),
        migrations.AddField(
            model_name='approver',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='question_approver', to='dt_planner_app.Question'),
        ),
        migrations.AddField(
            model_name='approver',
            name='reasons',
            field=models.ManyToManyField(blank=True, related_name='reason_approver', to='dt_planner_app.Reason'),
        ),
        migrations.AddField(
            model_name='approver',
            name='types',
            field=models.ManyToManyField(blank=True, related_name='type_approver', to='dt_planner_app.Type'),
        ),
        migrations.AddField(
            model_name='approver',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_approver', to='dt_planner_app.user'),
        ),
    ]
