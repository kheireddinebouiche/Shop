# Generated by Django 3.1.4 on 2021-08-16 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210816_0100'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentairesProduits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentaires', models.TextField(blank=True, max_length=1000, null=True)),
                ('nom_client', models.CharField(blank=True, max_length=100, null=True)),
                ('email_client', models.EmailField(blank=True, max_length=1000, null=True)),
                ('produit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.produit')),
            ],
            options={
                'verbose_name': 'Commentaire produit',
                'verbose_name_plural': 'Commentaires produits',
            },
        ),
    ]
