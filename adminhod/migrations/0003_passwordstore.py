# Generated by Django 4.0.5 on 2022-08-23 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminhod', '0002_alter_customuser_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PasswordStore',
                'verbose_name_plural': 'PasswordStores',
            },
        ),
    ]
