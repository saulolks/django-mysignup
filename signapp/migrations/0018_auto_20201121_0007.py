# Generated by Django 3.1.3 on 2020-11-21 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signapp', '0017_auto_20201121_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='hash',
            field=models.CharField(default='928fe738-9103-41c2-aaa0-d5c598fa4738', max_length=100, unique=True),
        ),
    ]
