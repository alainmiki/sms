# Generated by Django 4.0.5 on 2022-08-30 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0004_period_alter_timetable_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalTimetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.period')),
                ('staff_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.timetable')),
            ],
            options={
                'verbose_name': 'FinalTimetable',
                'verbose_name_plural': 'FinalTimetables',
            },
        ),
    ]
