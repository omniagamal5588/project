# Generated by Django 4.1.7 on 2023-05-06 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_address_user_last_name_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Address'),
        ),
    ]
