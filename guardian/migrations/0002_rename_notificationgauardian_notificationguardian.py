# Generated by Django 4.0.5 on 2022-08-11 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_studentgovernment_created_at'),
        ('guardian', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NotificationGauardian',
            new_name='NotificationGuardian',
        ),
    ]
