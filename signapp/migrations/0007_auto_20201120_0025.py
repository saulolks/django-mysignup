# Generated by Django 3.1.3 on 2020-11-20 00:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('signapp', '0006_auto_20201120_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
