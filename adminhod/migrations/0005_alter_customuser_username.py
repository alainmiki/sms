# Generated by Django 4.0.5 on 2023-08-21 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhod', '0004_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
