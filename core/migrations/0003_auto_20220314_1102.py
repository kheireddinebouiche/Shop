# Generated by Django 3.1 on 2022-03-14 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220314_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepanier',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='panier',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]
