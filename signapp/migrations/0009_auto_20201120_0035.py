# Generated by Django 3.1.3 on 2020-11-20 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signapp', '0008_auto_20201120_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='hash',
            field=models.CharField(default='<function uuid4 at 0x7fcf30e49bf8>', max_length=100, unique=True),
        ),
    ]
