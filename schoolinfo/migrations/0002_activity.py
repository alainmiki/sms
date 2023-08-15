# Generated by Django 4.0.5 on 2022-08-11 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
        ),
    ]
