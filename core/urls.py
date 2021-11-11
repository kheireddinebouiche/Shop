from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import *

app_name='core'

urlpatterns = [ 

    path('', Index, name='index'),
    path('<int:pk>/details-produit/', ProductDetails, name="details-produit"),
    path('Boutique-g/', VoirLaBoutique, name='boutique'),
    path('Boutique-l/', ShopList, name='boutique-list'),
]

