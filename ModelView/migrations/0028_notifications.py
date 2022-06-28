# Generated by Django 3.2 on 2021-11-06 13:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ModelView', '0027_alter_useraccounts_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('username', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('order_id', models.CharField(blank=True, max_length=200, null=True)),
                ('notification_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Notifications',
            },
        ),
    ]