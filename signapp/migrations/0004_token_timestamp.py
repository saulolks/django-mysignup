# Generated by Django 3.1.3 on 2020-11-18 23:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('signapp', '0003_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='timestamp',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
