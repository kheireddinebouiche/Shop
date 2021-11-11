from django.db import models
from django.db.models import base
from django.db.models.base import Model
from django.db.models.fields.files import ImageField
from django.utils import timezone




SHIP ={
    ('fr', 'Livraison gratuite'),
    ('py', 'Livraion payante'),
}

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

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.designation

class CommentairesProduits(models.Model):
    produit = models.ForeignKey(Produit, null=True, blank=True, on_delete=models.CASCADE)
    commentaires = models.TextField(max_length=1000, null=True, blank=True)
    nom_client = models.CharField(max_length=100, null=True, blank=True)
    email_client = models.EmailField(max_length=1000, null=True, blank=True)

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
    image1 = ImageField(null=True, blank=True)
    image2 = ImageField(null=True, blank=True)
    image3 = ImageField(null=True, blank=True)
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





    

