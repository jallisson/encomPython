# Generated by Django 2.1.7 on 2019-03-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encom', '0010_auto_20190304_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='qtde',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='venda',
            name='responsavel_frete',
            field=models.CharField(choices=[('REMETENTE', 'REMETENTE'), ('DESTINATARIO', 'DESTINATARIO'), ('REDESPACHO', 'REDESPACHO')], default='REMETENTE', max_length=14),
        ),
    ]