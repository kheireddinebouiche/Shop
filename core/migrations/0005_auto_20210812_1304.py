# Generated by Django 3.1.4 on 2021-08-12 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_collectionproduit'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionproduit',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='collectionproduit',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]