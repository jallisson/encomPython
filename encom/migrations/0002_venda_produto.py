# Generated by Django 2.1.5 on 2019-02-05 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('encom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='produto',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='encom.Produto'),
        ),
    ]