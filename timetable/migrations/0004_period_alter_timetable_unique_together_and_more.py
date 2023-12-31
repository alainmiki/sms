# Generated by Django 4.0.5 on 2022-08-30 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_alter_timetable_unique_together_alter_timetable_day_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
            options={
                'verbose_name': 'Period',
                'verbose_name_plural': 'Periods',
            },
        ),
        migrations.AlterUniqueTogether(
            name='timetable',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='start_time',
        ),
    ]
