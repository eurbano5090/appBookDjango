from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Book


class formBook(forms.ModelForm):
   #extructuras para agregar validaciones
   valoracion = forms.IntegerField(
       label= 'Valoración',
       widget= forms.NumberInput(attrs={'class':'form-control  w-25'}),
       help_text='valoracion entre 0 y 100',
       validators=[MinValueValidator(0), MaxValueValidator(100)]
   )

   class Meta: #para establecer caracteristicas formulario
       model = Book  #modelo al que pertenece el formulario
       fields = ['titulo','autor','valoracion']
       labels = {
           'titulo': 'Titulo',
           'autor': 'Autor'
       }
       widgets = {
           'titulo': forms.TextInput(attrs={'class':'form-control w-100'}),
           'autor': forms.TextInput(attrs={'class':'form-control w-100'}),
       #    'valoracion':forms.NumberInput(attrs={'class':'form-control','style':'width : 300px'})
       }
