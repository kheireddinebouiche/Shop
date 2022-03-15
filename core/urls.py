from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import *
from django.contrib.auth.views import LoginView, LogoutView

app_name='core'

urlpatterns = [ 

    path('', Index, name='index'),
    path('<int:pk>/details-produit/', ProductDetails, name="details-produit"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('Boutique-g/', VoirLaBoutique, name='boutique'),
    path('Boutique-l/', ShopList, name='boutique-list'),
    path('inscription/', InscriptionClient, name="inscription-client"),

    path('mon-compte/', MonCompte, name="mon-compte"),
    path('wishliste/', Whishlist, name="wishliste"),
    path('ajouter-a-la-liste-des-envies/<int:pk>/', AddToWhishlist, name="ajouter-wishliste"),
    path('supprimer-de-ma-liste/<int:pk>/', RemoveFromWishliste, name="supprimer-de-ma-liste"),
    path('confirmer-ma-commande/', PasserCommande, name="passer-commande"),
    path('mon-panier/', ViewPanier, name="mon-panier"),
    path('ajouter-au-panier/<int:pk>/', AddToPanier, name="ajouter-au-panier"),
]

