
from django.http import request
from django.shortcuts import render
from core.models import *


def Index(request):
    product = Produit.objects.filter(af_du_jour=True)[:8]
    categories = Categories.objects.filter(sous_cat__isnull = True)[:11]
    
    context={
        'product': product,
        'categories': categories,
    }

    return render(request, 'front/market1.html', context)

def VoirPlusAffaire(request):
    product = Produit.objects.all()
    context={
        'product' : product
    }
    return render(request, 'front/list-affaire-du-jour.html', context)


def ProductDetails(request, pk):
    produit = Produit.objects.get(id=pk)
   
  
    try:
        prev = Produit.objects.get(id=pk-1)
    except:
        prev = Produit.objects.get(id=pk)

    try:
        next = Produit.objects.get(id=pk+1)
    except:
        next = Produit.objects.get(id=pk)

    categories = Categories.objects.filter(sous_cat__isnull = True)[:11]

    c = [categories.desigantion for categories in produit.categories.all()]
    
    produits_connexe = Produit.objects.filter(categories__desigantion__in = c).distinct().order_by('-created_at')

    print(produits_connexe)
   
    context={
        'produit' : produit,
        'categories': categories,
        'produits_connexe' : produits_connexe,
        'prev': prev,
        'next' : next,
    }
    return render(request,'front/product-right-sidebar.html', context )


def VoirLaBoutique(request):
    return render(request,'front/shop.html')

def ShopList(request):
    return render(request, 'front/shop-list.html')

