# Generated by Django 5.1.3 on 2024-11-11 08:49

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_doctor_email_doctor_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+234', max_length=14, region=None),
        ),
    ]
