from django.contrib import admin
from . models import Pregunta, ElegirRespuesta, PreguntasRespondidas, QuizUsuario
from . forms import ElegirFormset

class ElegirInline(admin.TabularInline):
    model = ElegirRespuesta
    max_num = ElegirRespuesta.MAX_NUM
    min_num = ElegirRespuesta.MIN_NUM
    
class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (ElegirInline, )
    list_display = ["texto",]
    search_fields = ["texto", "preguntas__texto"]

class IntentoAdmin(admin.ModelAdmin):
    list_display = ["pregunta", "respuesta", "correcta"]
    class Meta:
        model = PreguntasRespondidas

admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(PreguntasRespondidas)
admin.site.register(QuizUsuario)
