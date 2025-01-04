from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Concurso

@admin.register(Concurso)
class ConcursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_concurso', 'nConcurso', 'bola1', 'bola2', 'bola3', 'bola4', 'bola5', 'bola6', 'bola7', 'bola8', 'bola9', 'bola10', 'bola11', 'bola12', 'bola13', 'bola14', 'bola15')
    list_filter = ('data_concurso', 'nConcurso')
    search_fields = ('id', 'data_concurso', 'nConcurso')
