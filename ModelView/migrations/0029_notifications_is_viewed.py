# Generated by Django 3.2 on 2021-11-06 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModelView', '0028_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='is_viewed',
            field=models.BooleanField(default=False),
        ),
    ]