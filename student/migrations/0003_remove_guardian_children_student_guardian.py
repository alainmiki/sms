# Generated by Django 4.0.5 on 2022-08-11 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_remove_student_guardian'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guardian',
            name='children',
        ),
        migrations.AddField(
            model_name='student',
            name='guardian',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='guardian', to='student.guardian'),
        ),
    ]
