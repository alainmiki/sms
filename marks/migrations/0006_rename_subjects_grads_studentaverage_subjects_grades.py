# Generated by Django 4.0.5 on 2022-10-05 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marks', '0005_alter_mark_semester_alter_studentaverage_semester_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentaverage',
            old_name='subjects_grads',
            new_name='subjects_grades',
        ),
    ]
