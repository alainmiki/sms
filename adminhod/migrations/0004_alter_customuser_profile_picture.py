# Generated by Django 4.0.5 on 2022-08-30 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhod', '0003_passwordstore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='static/images/default.jpg', null=True, upload_to='profile_pictures'),
        ),
    ]
