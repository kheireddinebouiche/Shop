from doctest import BLANKLINE_MARKER
from hashlib import blake2b
from pickle import TRUE
from tabnanny import verbose
from tkinter import N
from turtle import onclick, update
from django.db import models
from django.db.models import base
from django.db.models.base import Model
from django.db.models.fields.files import ImageField
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save


USER_STATUS = {
    ('cli', 'Client'),
    ('adm', 'Administrateur'),
}

SHIP ={
    ('fr', 'Livraison gratuite'),
    ('py', 'Livraion payante'),
}

PAIEMENT = {
    ('liv', 'Paiement à la livraison'),
    ('ccp', 'Virement CCP'),
    ('rib', 'Virement Bancaire'),
}


class Localite(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name="Localité"
        verbose_name_plural="Localitées"

    def __str__(self):
        return self.label

class Pays(models.Model):
    label = models.CharField(max_length=40, null=True, blank=True)
    code_court = models.CharField(max_length=3, null=True, blank=True)
    localite = models.ManyToManyField(Localite)

    class Meta:
        verbose_name="Pays"
        verbose_name_plural="Pays"
    
    def __str__(self):
        return self.label

class ZoneLivraison(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    localite = models.ManyToManyField(Localite)
    montant = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name="Zone de livraison"
        verbose_name_plural = "Zones de livraisons"

    def __str__(self):
        return self.label

class Monnaie(models.Model):
    label = models.CharField(max_length=4, null=True, blank=True)

    class Meta:
        verbose_name="Monnaie"
        verbose_name_plural="Monnaies"

    def __str__(self):
        return self.label

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_identification = models.CharField(max_length=40, null=True,blank=True)
    adresse = models.CharField(max_length=200, null=True,blank=True)
    localite = models.ForeignKey(Localite, null=True, blank=True, on_delete=models.CASCADE)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, blank=True, null=True)
    num_tel = models.CharField(max_length=12,null=True,blank=True)
    image = models.ImageField(null=True, blank=True)
    user_type = models.CharField(max_length=3, choices=USER_STATUS, blank=True, null=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    code_access = models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.num_identification)
        super(Profile, self).save(*args, **kwargs)

class Produit(models.Model):
    designation = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    longue_description = models.TextField(max_length=600, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    prix = models.FloatField(null=True, blank=True)
    prix_promo = models.FloatField(null=True, blank=True)
    fabricant = models.CharField(max_length=100, null=True, blank=True)
    couleurs = models.ManyToManyField('Couleurs', blank=True)
    marque = models.ForeignKey('Marque', null=True, blank=True, on_delete=models.CASCADE)

    condition_livraison = models.ForeignKey('ConditionLivraison', null=True, blank=True, on_delete=models.DO_NOTHING )
    condition_paiement = models.ForeignKey('ConditionPaiement', null=True, blank=True, on_delete=models.DO_NOTHING)
    condition_retour = models.ForeignKey('CondtionDeRetour', null=True, blank=True, on_delete=models.DO_NOTHING)

    label = models.ManyToManyField('LabelProduit', blank=True)

    categories = models.ManyToManyField('Categories', blank=True)

    mise_en_avant = models.BooleanField(default=False, null=True, blank=True)
    af_du_jour = models.BooleanField(default=False, null=True, blank=True)

    taille = models.ManyToManyField("Taille", blank=True)
    poids = models.FloatField(null=True, blank=True)
    longeur = models.FloatField(null=True, blank=True)
    largeur = models.FloatField(null=True, blank=True)
    hauteur = models.FloatField(null=True, blank=True)

    materiel = models.ManyToManyField("Materiel", blank=True)

    autoriser_commentaire = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.designation

class CommentairesProduits(models.Model):
    produit = models.ForeignKey(Produit, null=True, blank=True, on_delete=models.CASCADE)
    commentaires = models.TextField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name="Commentaire produit"
        verbose_name_plural = "Commentaires produits"

    def __str__(self):
        return self.produit

class LabelProduit(models.Model):
    designation = models.CharField(max_length=100, null=True, blank=True)
    couleur_tag = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name="Tag de produit"
        verbose_name_plural = "Tags des produits"

    def __str__(self):
        return self.designation

class Taille(models.Model):
    designation = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name="taille"
        verbose_name_plural="tailles"

    def __str__(self):
        return self.designation

class Materiel(models.Model):
    designation = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name="matériel"
        verbose_name_plural="matériaux"
    
    def __str__(self):
        return self.designation

class ConditionLivraison(models.Model):
    livraison = models.CharField(max_length=200, null=True, blank=True)
    autres = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Condition de livraison"
        verbose_name_plural="Conditions de livraison"

    def __str__(self):
        return self.livraison

class ConditionPaiement(models.Model):
    paiement = models.CharField(max_length=200, null=True, blank=True)
    autres = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Condition de paiement"
        verbose_name_plural = "Conditions de paiement"

    def __str__(self):
        return self.paiement

class CondtionDeRetour(models.Model):
    retour = models.CharField(max_length=200, null=True, blank=True)
    autres = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Condition de retour"
        verbose_name_plural="Conditions de retour"

    def __str__(self):
        return self.retour

class AffaireDuJour(models.Model):
    product = models.ForeignKey(Produit, null=True, blank=True, on_delete=models.DO_NOTHING)
    is_aff_du_jour = models.BooleanField(default=False, null=True, blank=True)
    is_mise_avant = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product

class Couleurs(models.Model):
    designation = models.CharField(max_length=100, null=True, blank=True)
    code_couleur = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.designation

class Marque(models.Model):
    designation = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Marque"
        verbose_name_plural="Marques"

    def __str__(self):
        return self.designation

class Categories(models.Model):
    desigantion = models.CharField(max_length=100, null=True, blank=True)
    sous_cat = models.ForeignKey('self', null=True, blank=True ,on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Catégorie"
        verbose_name_plural="Catégories"

    def __str__(self):
        return self.desigantion

class ProductImageVariation(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    image = ImageField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Variation de produit"
        verbose_name_plural="Variations des produits"

    def __stre__(self):
        return self.produit

class CollectionProduit(models.Model):
    designation = models.CharField(max_length=200, null=True, blank=True)
    produit = models.ManyToManyField(Produit, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name="Collection"
        verbose_name_plural="Colléctions"

    def __str__(self):
        return self.designation

############ MODEL WISHLISTE ######################
class ProduitWishliste(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, null=True, blank=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        verbose_name="Article wishliste"
        verbose_name_plural= "Articles wishliste"

    def __str__(self):
        return self.produit.designation
class Wishlist(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    produit = models.ManyToManyField(ProduitWishliste)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Liste d'envies"
        verbose_name_plural="listes d'envies"

    def __str__(self):
        return self.user.username
############ FIN MODEL WISHLISTE ##################

############ MODEL PANIER #########################
class ArticlePanier(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, null=True, blank=True, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    total = models.FloatField(null=True, blank=True)
    ordered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_item_price(self):
        return self.quantite * self.produit.prix

    class Meta:
        verbose_name="Article du panier"

    def __str__(self):
        return self.produit.designation

class Panier(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    articles = models.ManyToManyField(ArticlePanier)
    total = models.FloatField(null=True, blank=True)
    adresse_livraison = models.CharField(max_length=1000, null=True, blank=True)
    mode_paiement = models.CharField(max_length=3, choices=PAIEMENT, null=True, blank=True)
    frais_livraison = models.FloatField(null=True, blank=True)
    ordered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        total = 0
        for order_item in self.articles.all():
            total += order_item.get_total_item_price()
        return total

    class Meta:
        verbose_name="Panier"
        verbose_name_plural="Paniers"

    def __str__(self):
        return self.user.username

########### FIN MODEL PANIER #####################

########## MODEL VUE RECEMMENT ###################
class RecentlyViewsPorduct(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name="Article Vue récemmment"
    
    def __str__(self):
        return self.produit.designation

class RecentlyViwed(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    produit = models.ManyToManyField(RecentlyViewsPorduct)

    class Meta:
        verbose_name="Liste Artcile vue récemment"

    def __str__(self):
        return self.user.username
########## FIN MODEL VUE RECEMMENT ###############