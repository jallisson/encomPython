# Generated by Django 2.1.7 on 2019-04-02 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encom', '0047_auto_20190402_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='hora_saida',
            field=models.TimeField(max_length=6),
        ),
    ]