from socket import fromshare
from django import forms
from .models import *
from django.forms import ModelForm, TextInput, EmailInput, widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField


USER_STATUS = {
    ('cli', 'Client'),
    ('adm', 'Administrateur'),
}

class ClientCreationForm(UserCreationForm):
    num_identification = forms.CharField(max_length=100, widget=widgets.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "N° d'identification national ou permie de conduire.",
        'label' : 'N° indentification'
    }))
    image = forms.ImageField()
   
    class Meta:
      model = User
      fields = ('username','email','first_name','last_name','num_identification', 'image')
      field_classes = {
          'username' : UsernameField,      
        }
      widgets = {
          'username' : TextInput(attrs={
              'class' : 'form-control',
              'placeholder': "Veuillez renseignez un nom d'utilisateur.",
          }),
          'email' : EmailInput(attrs={
              'class' : 'form-control',
              'placeholder': "Adresse email de l'utilisateur",
          }),
          'first_name' : TextInput(attrs={
              'class' : 'form-control',
              'placeholder' : 'Prénom',
          }),
          'last_name' : TextInput(attrs={
              'class' : 'form-control',
              'placeholder' : "Nom de l'utilisateur."
          }),
            
      }
