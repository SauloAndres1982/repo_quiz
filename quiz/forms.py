from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from .models import Pregunta, ElegirRespuesta, PreguntasRespondidas

User = get_user_model()

class ElegirFormset(forms.BaseInlineFormSet):
    
    def clean(self):
        super(ElegirFormset, self).clean()        
        respuesta_correcta = 0
        for formulario in self.forms:
            if not formulario.is_valid():
                return 
            
            if formulario.cleaned_data and formulario.cleaned_data.get("correcta") is True:
                respuesta_correcta += 1
                
        try:
            assert respuesta_correcta == Pregunta.NUMERO_DE_RESPUESTAS_PERMITIDAS
        except AssertionError:
            raise forms.ValidationError("Exactamente una sola respuesta es permitida")
        
class UsuarioLoginFormulario(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Este usuario no existe")
            
            if not user.check_password(password):
                raise forms.ValidationError("Contraseña incorrecta")
            
            if not user.is_active:
                raise forms.ValidationError("Este usuario no está activo")
                
            
class RegistroFormulario(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",                
        ]