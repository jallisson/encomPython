# Generated by Django 2.1.7 on 2019-04-19 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encom', '0050_auto_20190419_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
