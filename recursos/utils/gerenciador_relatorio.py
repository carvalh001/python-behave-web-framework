import json
import platform
import psutil
import socket
import sys
from datetime import datetime
from pathlib import Path


class GerenciadorDeRelatorio:
    """
    Gerencia a coleta de metadados e informações para geração de relatórios.
    Coleta dados do sistema, ambiente de teste e execução.
    """
    
    def __init__(self, configuracao):
        """
        Inicializa o gerenciador de relatório
        
        Args:
            configuracao: Instância de GerenciadorDeConfiguracao
        """
        self.configuracao = configuracao
        self.horario_inicio = None
        self.horario_fim = None
        self.duracao_total = None
        self.informacoes_sistema = {}
        self.informacoes_ambiente_teste = {}
        self.informacoes_navegador = {}
    
    def registrar_inicio_execucao(self):
        """Registra o horário de início da execução dos testes"""
        self.horario_inicio = datetime.now()
        print(f"[RELATÓRIO] Execução iniciada: {self.horario_inicio.strftime('%d/%m/%Y %H:%M:%S')}")
        
        self._coletar_informacoes_sistema()
        self._coletar_informacoes_ambiente()
    
    def registrar_fim_execucao(self):
        """Registra o horário de término e calcula a duração total"""
        self.horario_fim = datetime.now()
        self.duracao_total = (self.horario_fim - self.horario_inicio).total_seconds()
        
        duracao_formatada = self._formatar_duracao(self.duracao_total)
        
        print("\n" + "="*60)
        print("EXECUÇÃO FINALIZADA")
        print("="*60)
        print(f"Duração Total: {duracao_formatada}")
        print(f"Início: {self.horario_inicio.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Término: {self.horario_fim.strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*60 + "\n")
    
    def registrar_informacoes_navegador(self, informacoes_navegador):
        """
        Armazena as informações do navegador coletadas pelo GerenciadorDeNavegador
        
        Args:
            informacoes_navegador: Dict com informações do navegador
        """
        self.informacoes_navegador = informacoes_navegador
    
    def _coletar_informacoes_sistema(self):
        """Coleta informações sobre o sistema operacional e hardware"""
        try:
            import os
            
            self.informacoes_sistema = {
                'sistema_operacional': platform.system(),
                'versao_sistema': platform.version(),
                'release_sistema': platform.release(),
                'versao_python': platform.python_version(),
                'processador': platform.processor(),
                'nucleos_cpu': psutil.cpu_count(logical=False),
                'threads_cpu': psutil.cpu_count(logical=True),
                'ram_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'hostname': platform.node(),
                'usuario': os.getlogin() if hasattr(os, 'getlogin') else 'Desconhecido'
            }
            
            print(f"[SISTEMA] {self.informacoes_sistema['sistema_operacional']} {self.informacoes_sistema['release_sistema']}")
            print(f"[SISTEMA] CPU: {self.informacoes_sistema['nucleos_cpu']} núcleos / {self.informacoes_sistema['threads_cpu']} threads")
            print(f"[SISTEMA] RAM: {self.informacoes_sistema['ram_total_gb']} GB")
            
        except Exception as erro:
            print(f"[SISTEMA] Erro ao coletar informações: {erro}")
            self.informacoes_sistema = {}
    
    def _coletar_informacoes_ambiente(self):
        """Coleta informações sobre o ambiente de teste"""
        try:
            self.informacoes_ambiente_teste = {
                'url_teste': self.configuracao.url_base_sistema,
                'diretorio_execucao': str(Path.cwd()),
                'caminho_python': sys.executable,
                'timezone': str(datetime.now().astimezone().tzinfo),
                'endereco_ip': socket.gethostbyname(socket.gethostname()),
                'linha_comando': ' '.join(sys.argv)
            }
            
        except Exception as erro:
            print(f"[AMBIENTE] Erro ao coletar informações: {erro}")
            self.informacoes_ambiente_teste = {}
    
    def salvar_metadados(self):
        """Salva todos os metadados em um arquivo JSON para uso no relatório"""
        try:
            metadados = {
                'execucao': {
                    'horario_inicio': self.horario_inicio.isoformat() if self.horario_inicio else None,
                    'horario_fim': self.horario_fim.isoformat() if self.horario_fim else None,
                    'duracao_segundos': self.duracao_total
                },
                'sistema': self.informacoes_sistema,
                'navegador': self.informacoes_navegador,
                'ambiente_teste': self.informacoes_ambiente_teste
            }
            
            arquivo_metadados = self.configuracao.diretorio_metadados / 'metadata_temp.json'
            arquivo_metadados.parent.mkdir(exist_ok=True, parents=True)
            
            with open(arquivo_metadados, 'w', encoding='utf-8') as arquivo:
                json.dump(metadados, arquivo, indent=2, ensure_ascii=False)
            
            print(f"[RELATÓRIO] Metadados salvos: {arquivo_metadados}")
            
        except Exception as erro:
            print(f"[RELATÓRIO] Erro ao salvar metadados: {erro}")
    
    def _formatar_duracao(self, segundos):
        """
        Formata duração em segundos para formato HH:MM:SS
        
        Args:
            segundos: Duração em segundos
            
        Returns:
            String formatada (ex: "01:23:45")
        """
        if not segundos:
            return "00:00:00"
        
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segundos_restantes = int(segundos % 60)
        
        return f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d}"
    
    def obter_resumo_execucao(self):
        """
        Retorna um dicionário com resumo da execução
        
        Returns:
            Dict com informações resumidas
        """
        return {
            'inicio': self.horario_inicio.strftime('%d/%m/%Y %H:%M:%S') if self.horario_inicio else 'N/A',
            'fim': self.horario_fim.strftime('%d/%m/%Y %H:%M:%S') if self.horario_fim else 'N/A',
            'duracao': self._formatar_duracao(self.duracao_total) if self.duracao_total else 'N/A',
            'sistema': self.informacoes_sistema.get('sistema_operacional', 'Desconhecido'),
            'navegador': self.informacoes_navegador.get('navegador', 'Desconhecido')
        }

