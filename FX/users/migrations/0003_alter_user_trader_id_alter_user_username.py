# Generated by Django 5.0.2 on 2024-07-15 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='trader_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
