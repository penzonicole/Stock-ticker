from decimal import Decimal, InvalidOperation
import os
import requests
from django.core.management.base import BaseCommand
from painel.models import RegistroCotacao

class Command(BaseCommand):
    help = 'Busca as cotações mais recentes na AwesomeAPI e grava no banco de dados em segundo plano.'

    def handle(self, *args, **options):
        url_multipla = os.environ.get(
            "COTACAO_URL", 
            "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL"
        )
        
        self.stdout.write(self.style.NOTICE('Iniciando busca automática de cotações...'))
        
        try:
            resposta = requests.get(url_multipla, timeout=5)
            resposta.raise_for_status()
            dados = resposta.json()
            
            registros_criados = 0
            for chave, info in dados.items():
                valor = Decimal(info['bid'])
                RegistroCotacao.objects.create(
                    moeda_origem=info['code'],
                    moeda_destino=info['codein'],
                    valor=valor
                )
                registros_criados += 1
                
            self.stdout.write(
                self.style.SUCCESS(f'Sucesso! {registros_criados} cotações atualizadas e salvas no banco de dados.')
            )
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Falha na requisição à API externa: {e}')
            )
        except (ValueError, KeyError, TypeError, InvalidOperation) as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao processar dados recebidos: {e}')
            )