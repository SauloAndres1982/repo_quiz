from django.shortcuts import render, HttpResponse, redirect
from .forms import RegistroFormulario, UsuarioLoginFormulario
from django.contrib.auth import get_user_model, authenticate, login, logout
from . models import QuizUsuario, Pregunta, PreguntasRespondidas
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


def inicio(request):    
    context = {
        "bienvenido": "Bienvenido"
    }
    return render(request, "inicio.html", context)

def homeUsuario(request):
    return render(request, "Usuario/home.html")

def jugar(request):
    quizUsuario, created = QuizUsuario.objects.get_or_create(usuario=request.user)
    
    if request.method == "POST":
        pregunta_pk = request.POST.get("pregunta_pk")
        pregunta_respondida = quizUsuario.intentos.select_related("pregunta").get(pregunta__pk=pregunta_pk)
        respuesta_pk = request.POST.get("respuesta_pk")     
        
        try:
            opcion_seleccionada = pregunta_respondida.pregunta.preguntas.get(pk=respuesta_pk)
        except ObjectDoesNotExist:
            raise Http404 
        
        QuizUsuario.validar_intentos(pregunta_respondida, opcion_seleccionada)
        
        return redirect(pregunta_respondida)  
        
    else:
        pregunta = quizUsuario.nuevas_preguntas()
        if pregunta is not None:
            quizUsuario.crear_intentos(pregunta)
        context = {
            "pregunta": pregunta            
        }        
    return render(request, "play/jugar.html", context)

def loginView(request):
    titulo = "login"
    form = UsuarioLoginFormulario(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username") 
        password = form.cleaned_data.get("password")
        usuario = authenticate(username=username, password=password)
        login(request, usuario)
        return redirect("home")
    
    context = {
        "form": form, 
        "titulo": titulo
    }
    return render(request, "Usuario/login.html", context)

def registro(request):
    titulo = "Crear una cuenta"
    if request.method == "POST":
        form = RegistroFormulario(request.POST)
        if form.is_valid():  
            form.save()
            return redirect("login")        
    else:
        form = RegistroFormulario()        
    context = {
        "form": form,
        "título": titulo
    }
    return render(request, "Usuario/registro.html", context)

def logoutView(request):
    logout(request)
    return redirect("/")