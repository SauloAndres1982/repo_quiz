from django.db import models
from django.contrib.auth.models import User
import random


class Pregunta(models.Model):
    
    NUMERO_DE_RESPUESTAS_PERMITIDAS = 1
    texto = models.TextField(verbose_name="Texto")
    max_puntaje = models.DecimalField(verbose_name="Máximo puntaje", default=3, decimal_places=2, max_digits=6)
    
    def __str__(self):
        return self.texto
    
class ElegirRespuesta(models.Model):
    
    MIN_NUM = 4
    MAX_NUM = 4    
    pregunta = models.ForeignKey(Pregunta, related_name="preguntas", on_delete=models.CASCADE)
    correcta = models.BooleanField(default=False, null=False, verbose_name="¿Es ésta la pregunta correcta?")
    texto = models.TextField(verbose_name="Texto respuestas")
    
    def __str__(self):
        return self.texto

class QuizUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntaje_total = models.DecimalField(verbose_name="Puntaje Total", default=0, decimal_places=2, max_digits=5)
    
    def nuevas_preguntas(self):
        respondidas = PreguntasRespondidas.objects.filter(quizUser=self).value_list("pregunta__pk", flat=True)
        preguntas_resultantes = Pregunta.objects.exclude(pk__in=respondidas)
        if not preguntas_resultantes.exists():
            return None
        return random.choice(preguntas_resultantes)
    
    def crear_intentos(self, pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta, QuizUsuario=self)
        intento.save()
        
    def validar_intentos(self, pregunta_respondida, respuesta_seleccionada):
        if pregunta_respondida.pregunta_id != respuesta_seleccionada.pregunta_id:
            return 
    
        pregunta_respondida.respuesta_seleccionada = respuesta_seleccionada
        if respuesta_seleccionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.max_puntaje
            
        pregunta_respondida.save()
        
    
class PreguntasRespondidas(models.Model):
    usuarios = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, related_name="intentos")
    correcta = models.BooleanField(default=False, verbose_name="¿Es esta la respuesta correcta?", null=False)
    puntaje_obtenido = models.DecimalField(verbose_name="Puntaje obtenido", default=0, decimal_places=2, max_digits=6)
    
    def __str__(self):
        return self.pregunta