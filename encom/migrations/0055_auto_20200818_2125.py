# Generated by Django 2.2.1 on 2020-08-19 00:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('encom', '0054_manifesto_hora_manifesto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manifesto',
            name='hora_manifesto',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
