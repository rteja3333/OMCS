# Generated by Django 4.1.7 on 2023-04-03 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OMCS', '0002_alter_doctor_phone_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='certificate',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='pincode',
        ),
    ]
