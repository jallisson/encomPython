# Generated by Django 2.2.1 on 2020-07-28 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('encom', '0057_auto_20200728_1127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recebimento',
            options={},
        ),
        migrations.CreateModel(
            name='Manifesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_venda', models.DateField(auto_now_add=True, verbose_name='Data')),
                ('carro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encom.Carro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]