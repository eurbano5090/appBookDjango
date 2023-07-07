import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission


from .models import Book
from .forms import formBook
# Create your views here.
class IndexPageView(TemplateView):
    template_name = 'index.html'
@login_required
def lista_libros(request):
   libros = Book.objects.all()
   return render(request,'lista_libros.html',{'libros': libros})
@login_required
def crear_libro(request):
   if request.method == 'POST': #si la peticion es de tipo post
       form = formBook(request.POST)
       if form.is_valid():
           form.save()  #para crear libro en base de datos
           messages.success(request,'Libro agregado exitosamente')
           return redirect('lista_libros')  #redirijiendo a vista libros
       else:#crear mensaje de error para enviarlo a la vista
           messages.error(request,'error en datos ingresados, intente nuevamente')
           return HttpResponseRedirect(reverse(crear_libro))

   else : #si la peticion no es post
       form = formBook() #establecemos el formulario
       return render(request, 'crear_libro.html', {'form' : form })

@login_required
def editar_libro(request,libro_id):
    book = get_object_or_404(Book, id=libro_id)
    if request.method == 'POST':
        form = formBook(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.fecha_modificacion = datetime.datetime.now()
            book.save()
            messages.success(request,'libro editado exitosamente')
            return redirect('lista_libros')
        else:
            messages.error(request,'error en datos ingresados')
            return HttpResponseRedirect(reverse(editar_libro, args=[libro_id]))

    else:  # si la peticion no es post
        form = formBook(instance = book)  # establecemos el formulario
        return render(request, 'editar_libro.html', {'form': form , 'libro_id': libro_id})

@login_required
def eliminar_libro(request,libro_id):
    book = get_object_or_404(Book, id=libro_id)

    book.delete()
    messages.info(request, 'libro eliminado exitosamente')
    return redirect('lista_libros')

def buscar_libro(request):
    if request.method=='GET':
        query = request.GET.get('query')   #obteniendo lo que trae el get
        libros = Book.objects.filter(Q(titulo__icontains=query) | Q(autor__icontains=query))
        return render(request,'buscar_libro.html',{'libros': libros })

def registro(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            content_type = ContentType.objects.get_for_model(Book)
            permission = Permission.objects.get(
                codename="development",
                content_type=content_type,
            )
            user.user_permissions.add(permission)

            messages.success(request, 'Registro realizado exitosamente')
            return redirect('login')
    else:  # si la peticion no es post
        form = UserCreationForm() # establecemos el formulario
    return render(request, 'registro.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username'] # obteniendo lo que trae
        password = request.POST['password']
        user = authenticate(request, username=username , password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado exitosamente')
            return redirect('lista_libros')
        else:
            messages.error(request, 'credenciales invalidas')
            return render(request, 'login.html')
    # si la peticion no es post
    return render(request, 'login.html')


def cerrar_sesion(request):
    logout(request)
    return render(request,'login.html')

def home_page_not_login(request):
    return render(request, 'index.html')

def ver_libro(request,libro_id):
    book = get_object_or_404(Book, id=libro_id)

    return render(request,'ver_libro.html',{'book':book})


