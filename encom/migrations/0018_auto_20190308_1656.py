# Generated by Django 2.1.7 on 2019-03-08 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encom', '0017_auto_20190308_0002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venda',
            old_name='american_express',
            new_name='cartao',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='cred_shop',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='dinner_clubs',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='master_card',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='visa',
        ),
        migrations.AddField(
            model_name='venda',
            name='cartoes',
            field=models.CharField(choices=[('DINNER CLUBS', 'DINNER CLUBS'), ('AMERICAN EXPRESS', 'AMERICAN EXPRESS'), ('CRED SHOP', 'CRED SHOP'), ('MASTER CARD', 'MASTER CARD'), ('VISA', 'VISA')], default='DINNER CLUBS', max_length=30),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nome',
            field=models.CharField(max_length=50),
        ),
    ]