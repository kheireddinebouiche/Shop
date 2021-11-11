from django.contrib import admin
from .models import *


admin.site.register(Produit)
admin.site.register(Categories)
admin.site.register(Marque)
admin.site.register(Couleurs)
admin.site.register(ProductImageVariation)
admin.site.register(ConditionLivraison)
admin.site.register(ConditionPaiement)
admin.site.register(CondtionDeRetour)
admin.site.register(CollectionProduit)
admin.site.register(Taille)
admin.site.register(Materiel)
admin.site.register(LabelProduit)
admin.site.register(CommentairesProduits)

