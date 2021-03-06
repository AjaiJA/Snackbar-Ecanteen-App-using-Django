# Generated by Django 3.2 on 2021-10-19 02:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ModelView', '0003_alter_cart_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='Food_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='cart',
            name='User_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
