# Generated by Django 3.2 on 2021-10-27 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModelView', '0008_alter_orders_order_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_list',
            field=models.JSONField(),
        ),
    ]