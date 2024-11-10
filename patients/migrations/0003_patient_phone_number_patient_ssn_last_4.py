# Generated by Django 5.1.3 on 2024-11-09 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_alter_appointment_last_visit_procedures_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='phone_number',
            field=models.IntegerField(default=1111),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='ssn_last_4',
            field=models.CharField(default='4444', max_length=4),
        ),
    ]