# Generated by Django 3.1.4 on 2021-08-12 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210812_2334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taille',
            options={'verbose_name': ('Taille',), 'verbose_name_plural': 'Tailles'},
        ),
        migrations.AddField(
            model_name='taille',
            name='designation',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
