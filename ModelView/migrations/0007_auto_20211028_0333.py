# Generated by Django 3.2 on 2021-10-27 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModelView', '0006_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='food_id',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='rate',
        ),
        migrations.AddField(
            model_name='orders',
            name='order_list',
            field=models.JSONField(default=''),
        ),
    ]
