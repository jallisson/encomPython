# Generated by Django 2.2.1 on 2020-08-19 00:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('encom', '0055_auto_20200818_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manifesto',
            name='hora_manifesto',
            field=models.TimeField(default=django.utils.timezone.now, max_length=6),
        ),
    ]
