# Generated by Django 3.2 on 2021-11-06 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModelView', '0030_notifications_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='notification_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
