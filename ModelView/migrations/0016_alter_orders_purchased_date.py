# Generated by Django 3.2 on 2021-10-29 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModelView', '0015_alter_orders_purchased_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='purchased_date',
            field=models.DateTimeField(),
        ),
    ]