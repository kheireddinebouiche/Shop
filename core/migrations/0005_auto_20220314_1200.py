# Generated by Django 3.1 on 2022-03-14 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_auto_20220314_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentairesproduits',
            name='email_client',
        ),
        migrations.RemoveField(
            model_name='commentairesproduits',
            name='nom_client',
        ),
        migrations.AddField(
            model_name='commentairesproduits',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='produit',
            name='autoriser_commentaire',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='panier',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('rib', 'Virement Bancaire'), ('liv', 'Paiement à la livraison'), ('ccp', 'Virement CCP')], max_length=3, null=True),
        ),
    ]