# Generated by Django 4.0.5 on 2022-08-31 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_admission_guardian_profile_picture_and_more'),
        ('timetable', '0005_finaltimetable'),
    ]

    operations = [
        migrations.AddField(
            model_name='finaltimetable',
            name='class_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.classroom'),
        ),
    ]
