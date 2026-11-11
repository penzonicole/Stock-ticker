from decimal import Decimal, InvalidOperation
import os
import requests
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import generics
from .models import RegistroCotacao
from .serializers import RegistroCotacaoSerializer

def consultar_cotacao(request):
    contexto = {}
    url_multipla = settings.COTACAO_URL
    url_clima = settings.WEATHER_API_URL
    
    # 1. Consulta Cotações (com Cache)
    dados = cache.get('cotacoes_cache')
    usou_cache = True

    if not dados:
        usou_cache = False
        try:
            resposta = requests.get(url_multipla, timeout=5)
            resposta.raise_for_status()
            dados = resposta.json()
            cache.set('cotacoes_cache', dados, timeout=120)
        except requests.exceptions.RequestException:
            return render(request, 'painel/consultar.html', {
                'erro': 'Não foi possível consultar a cotação agora. Tente novamente em instantes.'
            })

    try:
        registros_criados = []
        for chave, info in dados.items():
            valor = Decimal(info['bid'])
            registro = RegistroCotacao.objects.create(
                moeda_origem=info['code'],
                moeda_destino=info['codein'],
                valor=valor
            )
            registros_criados.append(registro)
            
        contexto = {
            'sucesso': True, 
            'registros': registros_criados,
            'usou_cache': usou_cache
        }
    except (ValueError, KeyError, TypeError, InvalidOperation):
        contexto = {'erro': 'Erro ao processar os dados de cotação.'}

    # 2. Consulta API de Clima
    try:
        resp_clima = requests.get(url_clima, timeout=5)
        if resp_clima.status_code == 200:
            dados_clima = resp_clima.json()
            clima_atual = dados_clima.get('current_weather', {})
            contexto['clima'] = {
                'temperatura': clima_atual.get('temperature'),
                'vento': clima_atual.get('windspeed')
            }
    except Exception as e:
        contexto['erro_clima'] = "Não foi possível carregar o clima agora."

    return render(request, 'painel/consultar.html', contexto)

class HistoricoCotacaoView(generics.ListAPIView):
    """Somente leitura: histórico do mais recente para o mais antigo."""
    serializer_class = RegistroCotacaoSerializer
    def get_queryset(self):
        return RegistroCotacao.objects.order_by('-data_hora_consulta', '-id')