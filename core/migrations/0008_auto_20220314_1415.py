# Generated by Django 3.1 on 2022-03-14 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20220314_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Localite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Localité',
                'verbose_name_plural': 'Localitées',
            },
        ),
        migrations.AlterField(
            model_name='panier',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('rib', 'Virement Bancaire'), ('liv', 'Paiement à la livraison'), ('ccp', 'Virement CCP')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='recentlyviwed',
            name='produit',
            field=models.ManyToManyField(to='core.RecentlyViewsPorduct'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='produit',
            field=models.ManyToManyField(to='core.ProduitWishliste'),
        ),
        migrations.CreateModel(
            name='ZoneLivraison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('montant', models.FloatField(blank=True, null=True)),
                ('localite', models.ManyToManyField(to='core.Localite')),
            ],
            options={
                'verbose_name': 'Zone de livraison',
                'verbose_name_plural': 'Zones de livraisons',
            },
        ),
        migrations.AddField(
            model_name='pays',
            name='localite',
            field=models.ManyToManyField(to='core.Localite'),
        ),
    ]
