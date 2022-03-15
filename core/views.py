
from http.client import HTTPResponse
from django.http import request, HttpResponse
from django.shortcuts import render, redirect
from core.models import *
from django.contrib.auth.decorators import login_required
from .forms import *

def Index(request):
    product = Produit.objects.filter(af_du_jour=True)[:8]
    categories = Categories.objects.filter(sous_cat__isnull = True)[:11]
    try:
        panier = Panier.objects.get(user = request.user, ordered=False)

    except:

        context={
            'product': product,
            'categories': categories,          
        }

        return render(request, 'front/market1.html', context)

    context={
        'product': product,
        'categories': categories, 
        'panier': panier,         
    }

    return render(request, 'front/market1.html', context)

def VoirPlusAffaire(request):
    product = Produit.objects.all()
    context={
        'product' : product
    }
    return render(request, 'front/list-affaire-du-jour.html', context)


############## GESTION DES CLIENTS ###################################################################
def InscriptionClient(request):
    form = ClientCreationForm()
    if request.method == 'POST':
        form = ClientCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.num_identification = form.cleaned_data.get('num_identification')
            user.profile.user_type='cli'
            user.profile.image = form.cleaned_data.get('image')
            user.save()
            return redirect('core:index')
        else:
            return HttpResponse('Erreur lors traitement du texte')
    else:
        context = {
            'form' : form
        }
        return render(request, 'front/inscription-client.html', context)

############## FIN GESTION DES CLIENTS ###############################################################

######## Détails du produit avec intégration du model vue recemment ##################################
def ProductDetails(request, pk):

    try:
        panier = Panier.objects.get(user=request.user, ordered=False)

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
    
        context={
            'produit' : produit,
            'categories': categories,
            'produits_connexe' : produits_connexe,
            'prev': prev,
            'next' : next,
            'panier': panier,
        }
        return render(request,'front/product-right-sidebar.html', context )

    except:

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
    
        context={
            'produit' : produit,
            'categories': categories,
            'produits_connexe' : produits_connexe,
            'prev': prev,
            'next' : next,
           
        }
        return render(request,'front/product-right-sidebar.html', context)

######################################################################################################

################ AFFICHAGE DE LA BOUTIQUE #######################
def VoirLaBoutique(request):
    produit = Produit.objects.all()
    categories = Categories.objects.filter(sous_cat__isnull = True)[:11]
    try:
        panier = Panier.objects.get(user = request.user, ordered = False)

        context = {
             'produit': produit,
             'categories': categories,
             'panier' : panier,
        }
        return render(request, 'front/shop.html', context)

    except:
        context = {
            'produit': produit,
            'categories': categories,
        }
        return render(request,'front/shop.html',context)

def ShopList(request):
    produit = Produit.objects.all()
    categories = Categories.objects.filter(sous_cat__isnull = True)[:11]
    
    context = {
        'produit': produit,
        'categories': categories,
    }
    return render(request, 'front/shop-list.html', context)
################### FIN AFFICHAGE DE LA BOUTIQUE ####################

################### SECTION MON COMPTE ##############################
@login_required(login_url='/login/')
def MonCompte(request):
    categories = Categories.objects.filter(sous_cat__isnull = True)[:11]

    try:
        panier = Panier.objects.get(user = request.user, ordered=False)
        order = Panier.objects.filter(user = request.user, ordered=True)
        context = {
            'categories' : categories,
            'panier' : panier,
            'order' : order,
        }      
        return render(request, 'front/account.html', context)

    except:
        context = {
            'categories' : categories,            
        }
        return render(request, 'front/account.html', context) 
################### FIN SECTION MON COMPTE ##########################
###########  WISHLISTE ########################
@login_required(login_url='/login/')
def Whishlist(request):
    categories = Categories.objects.filter(sous_cat__isnull = True)[:11]
    wishliste = Wishlist.objects.get(user=request.user)

    context={
        'categories' : categories,
        'wishliste' : wishliste,
    }
    return render(request, 'front/wishlist.html', context)

@login_required(login_url='/login/')
def AddToWhishlist(request, pk):
    produit = Produit.objects.get(id=pk)   
    article_wishlist, created = ProduitWishliste.objects.get_or_create(user = request.user, produit = produit)
    wishlist_qs = Wishlist.objects.filter(user=request.user)

    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        wishlist.produit.add(article_wishlist)
        article_wishlist.save()
        return redirect('core:index')
    else:
        wishlist = Wishlist.objects.create(user = request.user)
        wishlist.produit.add(article_wishlist)
        return redirect('core:index')

@login_required(login_url='/login/')
def RemoveFromWishliste(request, pk):
    pass
######### FIN WISHLISTE ######################

######## PANIER #############################
@login_required(login_url='/login/')
def ViewPanier(request):

    try:
        panier = Panier.objects.get(user=request.user, ordered=False) 
        livraison = request.user.profile.localite.id
        zone = ZoneLivraison.objects.get(localite__id = livraison)
        panier.frais_livraison = zone.montant
        panier.total = panier.get_total() - zone.montant
        panier.save()

        context = {
            'panier' : panier,
        }
        return render(request, 'front/cart.html',context)

    except:
        return render(request, 'front/cart.html')

@login_required(login_url='/login/')
def AddToPanier(request, pk):
    produit = Produit.objects.get(id=pk)
    article_panier, created = ArticlePanier.objects.get_or_create(user=request.user,produit=produit,ordered = False,total=produit.prix)        
    order_qs = Panier.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.articles.filter(produit__id=produit.id).exists():
            article_panier.quantite += 1
            article_panier.save()
            return redirect('core:index')
        else:
            order.articles.add(article_panier)
            article_panier.save()
            return redirect('core:index')
    else:
        order = Panier.objects.create(user = request.user, ordered=False)
        order.articles.add(article_panier)
        return redirect('core:index')

@login_required(login_url='/login/')
def RemoveFromPanier(request, pk):
    pass

@login_required(login_url='/login')
def RemoveProductQuantite(request, pk):
    pass
    
######## FIN PANIER #########################################################

################ GESTION DES COMMANDES ######################################
def PasserCommande(request):
    try:
        panier = Panier.objects.get(user = request.user, ordered = False)
        context = {
            'panier' : panier,
        }
        return render(request, 'front/checkout.html', context)
    except:
        return render(request, 'front/checkout.html')
################ FIN GESTION DES COMMANDES ###################################

######## TABLEAU DE BORD DE GESTION ##########################################
def BackEndAdministrations(request):
    pass
######## FIN TABLEAU DE BORD DE GESTION ######################################