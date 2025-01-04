
from django.core.paginator import Paginator
import random
from django.shortcuts import render, redirect
from .models import *

from django.contrib import messages
# Create your views here.

from django import template
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from math import comb  # Importa para cálculo de combinações possíveis



register = template.Library()

@register.filter
def getattr_dynamic(obj, attr):
    return getattr(obj, attr, None)


def index(request):
    return render(request, 'index.html')



def home(request):
    return render(request, 'index.html')    

def home_view(request):
    # Adicione sua lógica aqui mais tarde
    pass

def concursos_view(request):
    # Número de linhas por página (padrão: 10)
    linhas_por_pagina = request.GET.get('linhas_por_pagina', 10)
    try:
        linhas_por_pagina = int(linhas_por_pagina)
    except ValueError:
        linhas_por_pagina = 10  # Caso não seja um número válido

    # Buscar todos os concursos e ordenar por número do concurso (decrescente)
    concursos = Concurso.objects.all().order_by('-nConcurso')

    # Configurar o Paginator
    paginator = Paginator(concursos, linhas_por_pagina)
    pagina = request.GET.get('page')
    concursos_paginados = paginator.get_page(pagina)

    # Renderizar o template
    return render(request, 'concurso.html', {
        'concursos': concursos_paginados,
        'linhas_por_pagina': linhas_por_pagina
    })


def jogos(request):
    jogos = Jogo.objects.filter(usuario=request.user).order_by('-data_criacao')  # Busca os jogos do usuário logado
    return render(request, 'jogos.html', {'jogos': jogos})


def login_view(request):
    # Adicione sua lógica aqui mais tarde
    pass

def signup_view(request):
    # Adicione sua lógica aqui mais tarde
    pass






def conferir_jogos(request):
    resultados = None
    dezenas = None

    if request.method == 'POST':
        dezenas = request.POST.get('dezenas', '').strip()
        dezenas_lista = [int(n.strip()) for n in dezenas.split(',') if n.strip().isdigit()]

        if len(dezenas_lista) != 15:
            messages.error(request, 'Por favor, insira exatamente 15 dezenas.')
            return render(request, 'jogos/conferirJogos.html', {'resultados': resultados, 'dezenas': dezenas})

        # Inicializa os contadores
        pontos = {'p15': 0, 'p14': 0, 'p13': 0, 'p12': 0, 'p11': 0}

        # Consulta todos os concursos no banco de dados
        concursos = Concurso.objects.all()

        for concurso in concursos:
            dezenas_concurso = {
                concurso.bola1, concurso.bola2, concurso.bola3, concurso.bola4, concurso.bola5,
                concurso.bola6, concurso.bola7, concurso.bola8, concurso.bola9, concurso.bola10,
                concurso.bola11, concurso.bola12, concurso.bola13, concurso.bola14, concurso.bola15,
            }

            # Calcula quantos números coincidem
            acertos = len(set(dezenas_lista) & dezenas_concurso)

            # Incrementa o contador baseado no número de acertos
            if acertos == 15:
                pontos['p15'] += 1
            elif acertos == 14:
                pontos['p14'] += 1
            elif acertos == 13:
                pontos['p13'] += 1
            elif acertos == 12:
                pontos['p12'] += 1
            elif acertos == 11:
                pontos['p11'] += 1

        resultados = pontos

    return render(request, 'jogos/conferirJogos.html', {'resultados': resultados, 'dezenas': dezenas})


from math import comb  # Importa para cálculo de combinações possíveis

def gerar_jogos(request):
    # ================================================
    # Debug inicial para acompanhar o fluxo
    print("DEBUG: Iniciando lógica de gerar_jogos...")

    # ================================================
    # Lógica para cálculo das combinações
    chance_15_pontos = comb(25, 15)  # Total de combinações possíveis para 15 pontos
    combinacoes_eliminadas = Concurso.objects.count()  # Total de combinações já premiadas

    # ================================================
    # Cálculo da nova probabilidade com o filtro
    if combinacoes_eliminadas > 0:
        nova_probabilidade = chance_15_pontos - combinacoes_eliminadas
        probabilidade_atual = nova_probabilidade
    else:
        probabilidade_atual = None

    # ================================================
    # Debug para acompanhar valores
    print(f"DEBUG: Total combinações possíveis: {chance_15_pontos}")
    print(f"DEBUG: Combinações eliminadas: {combinacoes_eliminadas}")
    print(f"DEBUG: Nova probabilidade: {nova_probabilidade}")
    print(f"DEBUG: Probabilidade atual: {probabilidade_atual}")

    # ================================================
    # Verifica se é um POST (Salvar Jogo)
    if request.method == 'POST':
        nome_jogo = request.POST.get('nomeJogo')
        concurso = request.POST.get('concurso')
        dezenas = request.POST.get('dezenas')
        filtro_15pontos = request.POST.get('filtro_15pontos') == 'on'

        dezenas_lista = [int(n.strip()) for n in dezenas.split(',') if n.strip().isdigit()]
        if len(dezenas_lista) != 15:
            messages.error(request, 'Por favor, insira exatamente 15 dezenas.')
            return redirect('gerar_jogos')

        # Filtro para eliminar combinações que já atingiram 15 pontos
        if filtro_15pontos:
            concursos = Concurso.objects.all()
            for concurso in concursos:
                if set(dezenas_lista) == {
                    concurso.bola1, concurso.bola2, concurso.bola3, concurso.bola4, concurso.bola5,
                    concurso.bola6, concurso.bola7, concurso.bola8, concurso.bola9, concurso.bola10,
                    concurso.bola11, concurso.bola12, concurso.bola13, concurso.bola14, concurso.bola15,
                }:
                    messages.error(request, 'Essa combinação já foi premiada com 15 pontos.')
                    return redirect('gerar_jogos')

        # Salvar o jogo
        Jogo.objects.create(
            usuario=request.user,
            nomeJogo=nome_jogo,
            nJogo=concurso,
            bola1=dezenas_lista[0],
            bola2=dezenas_lista[1],
            bola3=dezenas_lista[2],
            bola4=dezenas_lista[3],
            bola5=dezenas_lista[4],
            bola6=dezenas_lista[5],
            bola7=dezenas_lista[6],
            bola8=dezenas_lista[7],
            bola9=dezenas_lista[8],
            bola10=dezenas_lista[9],
            bola11=dezenas_lista[10],
            bola12=dezenas_lista[11],
            bola13=dezenas_lista[12],
            bola14=dezenas_lista[13],
            bola15=dezenas_lista[14],
        )

        messages.success(request, f'Jogo "{nome_jogo}" salvo com sucesso!')
        return redirect('meus_jogos')

    # ================================================
    # Renderizar template com valores atualizados
    return render(request, 'jogos/gerarJogos.html', {
        'chance_15_pontos': chance_15_pontos,
        'probabilidade_atual': probabilidade_atual,
        'combinacoes_eliminadas': combinacoes_eliminadas,
    })




def configuracoes(request):
    return render(request, 'configuracoes.html')


def meus_jogos(request):
    jogos = Jogo.objects.all()
    return render(request, 'jogos/meusjogos.html', {'jogos': jogos})



from django.contrib import messages
from .models import Jogo

def excluir_jogo(request, jogo_id):
    # Obter o jogo ou retornar erro 404
    jogo = get_object_or_404(Jogo, nJogo=jogo_id)
    
    # Excluir o jogo
    jogo.delete()
    messages.success(request, 'Jogo excluído com sucesso!')
    
    # Redirecionar para a página de "Meus Jogos"
    return redirect('meus_jogos')


from django.shortcuts import render
from django.db.models import Max
from .models import Concurso

def estatisticas(request):
    filtro_concursos = request.GET.get('filtro_concursos', None)
    resultados = {
        'mais_antigo': None,
        'mais_recente': None,
        'combinacao': None,
        'media_p15': 0,
        'media_p14': 0,
        'media_p13': 0,
        'media_p12': 0,
        'media_p11': 0,
    }

    if filtro_concursos:
        try:
            filtro_concursos = int(filtro_concursos)

            # Recuperar o último concurso registrado
            mais_recente = Concurso.objects.aggregate(Max('nConcurso'))['nConcurso__max']
            mais_antigo = max(mais_recente - filtro_concursos + 1, 1)

            concursos_filtrados = Concurso.objects.filter(nConcurso__gte=mais_antigo, nConcurso__lte=mais_recente)

            if concursos_filtrados.exists():
                resultados['mais_antigo'] = mais_antigo
                resultados['mais_recente'] = mais_recente

                # Obter a combinação do concurso mais recente
                concurso_recente = concursos_filtrados.order_by('-nConcurso').first()
                combinacao_recente = [
                    concurso_recente.bola1, concurso_recente.bola2, concurso_recente.bola3,
                    concurso_recente.bola4, concurso_recente.bola5, concurso_recente.bola6,
                    concurso_recente.bola7, concurso_recente.bola8, concurso_recente.bola9,
                    concurso_recente.bola10, concurso_recente.bola11, concurso_recente.bola12,
                    concurso_recente.bola13, concurso_recente.bola14, concurso_recente.bola15
                ]
                resultados['combinacao'] = combinacao_recente

                # Inicializar contadores para pontos
                total_pontos = {
                    'p15': 0,
                    'p14': 0,
                    'p13': 0,
                    'p12': 0,
                    'p11': 0,
                }
                
                for concurso in concursos_filtrados:
                    dezenas_concurso = {
                        concurso.bola1, concurso.bola2, concurso.bola3, concurso.bola4, concurso.bola5,
                        concurso.bola6, concurso.bola7, concurso.bola8, concurso.bola9, concurso.bola10,
                        concurso.bola11, concurso.bola12, concurso.bola13, concurso.bola14, concurso.bola15,
                    }

                    acertos = len(set(combinacao_recente) & dezenas_concurso)

                    if acertos == 15:
                        total_pontos['p15'] += 1
                    elif acertos == 14:
                        total_pontos['p14'] += 1
                    elif acertos == 13:
                        total_pontos['p13'] += 1
                    elif acertos == 12:
                        total_pontos['p12'] += 1
                    elif acertos == 11:
                        total_pontos['p11'] += 1

                # Calcular médias
                num_concursos = len(concursos_filtrados)
                resultados['media_p15'] = round(total_pontos['p15'] / num_concursos, 2)
                resultados['media_p14'] = round(total_pontos['p14'] / num_concursos, 2)
                resultados['media_p13'] = round(total_pontos['p13'] / num_concursos, 2)
                resultados['media_p12'] = round(total_pontos['p12'] / num_concursos, 2)
                resultados['media_p11'] = round(total_pontos['p11'] / num_concursos, 2)

        except ValueError:
            resultados['erro'] = "Por favor, insira um número válido de concursos."

    return render(request, 'jogos/estatisticas.html', resultados)
