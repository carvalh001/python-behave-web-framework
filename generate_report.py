#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gerador de Relatório HTML para resultados do Behave.
Lê o arquivo JSON e gera um HTML visual com suporte correto a UTF-8.
"""
import json
import unicodedata
from datetime import datetime
from pathlib import Path
import shutil
import os
import platform
import psutil
import selenium

def carregar_configuracoes_env():
    """
    Carrega configurações do arquivo .env para usar nas mensagens dinâmicas
    
    Returns:
        Dict com as configurações do .env
    """
    config = {}
    env_file = Path('.env')
    
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        except Exception as e:
            print(f"[AVISO] Erro ao carregar .env: {e}")
    
    return config


def generate_html_report(json_file='reports/results.json', output_file=None):
    """Gera relatório HTML a partir do JSON do Behave"""
    
    # Carrega configurações do .env para mensagens dinâmicas
    env_config = carregar_configuracoes_env()
    
    # Define a data e hora atuais
    now = datetime.now()
    
    # Mapeamento de meses em português
    meses = {
        '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril',
        '05': 'Maio', '06': 'Junho', '07': 'Julho', '08': 'Agosto',
        '09': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
    }
    
    # Cria estrutura de pastas: reports/2025/Outubro/Testes - 2025-10-15 16h32/
    year = now.strftime('%Y')
    month_num = now.strftime('%m')
    month_name = meses[month_num]
    
    # Pasta do dia com formato: "Testes - 2025-10-15 16h32"
    day_folder = now.strftime('Testes - %Y-%m-%d %Hh%M')
    
    report_dir = Path('reports') / year / month_name / day_folder
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Define nome do arquivo com timestamp: report_15-10-2025_14-30.html
    timestamp = now.strftime('%d-%m-%Y_%H-%M')
    
    if output_file is None:
        output_file = report_dir / f'report_{timestamp}.html'
    
    # Move o JSON para a pasta organizada
    json_destination = report_dir / f'results_{timestamp}.json'
    if Path(json_file).exists():
        shutil.copy2(json_file, json_destination)
        print(f"[OK] JSON copiado para: {json_destination}")
    
    # Move screenshots se existirem e mantém referência
    screenshots_src = Path('reports/screenshots')
    screenshots_dest = None
    screenshot_mapping = {}  # Mapeia nome original -> novo caminho relativo
    
    if screenshots_src.exists() and any(screenshots_src.iterdir()):
        screenshots_dest = report_dir / f'screenshots_{timestamp}'
        screenshots_dest.mkdir(parents=True, exist_ok=True)
        
        # Copia APENAS arquivos .png (evita copiar arquivos temporários)
        arquivos_copiados = 0
        for screenshot_file in screenshots_src.glob('*.png'):
            if screenshot_file.is_file():
                shutil.copy2(screenshot_file, screenshots_dest / screenshot_file.name)
                screenshot_mapping[screenshot_file.name] = f'screenshots_{timestamp}/{screenshot_file.name}'
                arquivos_copiados += 1
        
        print(f"[OK] {arquivos_copiados} screenshot(s) copiado(s) para: {screenshots_dest}")
        
        # Limpa diretório original após copiar
        for screenshot_file in screenshots_src.glob('*.png'):
            try:
                screenshot_file.unlink()
            except Exception:
                pass
    
    # Move vídeos se existirem e mantém referência
    videos_src = Path('reports/videos')
    videos_dest = None
    video_mapping = {}  # Mapeia nome original -> novo caminho relativo
    
    if videos_src.exists() and any(videos_src.iterdir()):
        videos_dest = report_dir / f'videos_{timestamp}'
        videos_dest.mkdir(parents=True, exist_ok=True)
        
        # Copia APENAS arquivos de vídeo (mp4, avi, webm)
        arquivos_video_copiados = 0
        for video_file in videos_src.iterdir():
            if video_file.is_file() and video_file.suffix in ['.mp4', '.avi', '.webm']:
                shutil.copy2(video_file, videos_dest / video_file.name)
                arquivos_video_copiados += 1
        
        print(f"[OK] {arquivos_video_copiados} vídeo(s) copiado(s) para: {videos_dest}")
        
        # Tenta converter vídeos com codecs problemáticos (FMP4, MP4V) para WebM
        # para melhor compatibilidade com navegadores
        try:
            from recursos.utils.video_converter import ensure_web_compatible_video
            
            videos_convertidos = 0
            for video_file in list(videos_dest.iterdir()):
                if video_file.is_file() and video_file.suffix in ['.mp4', '.avi']:
                    print(f"[INFO] Verificando compatibilidade: {video_file.name}")
                    compatible_path = ensure_web_compatible_video(str(video_file))
                    
                    # Se foi convertido para WebM, remove o MP4 original
                    if compatible_path != str(video_file) and Path(compatible_path).exists():
                        print(f"[INFO] ✓ Vídeo convertido para WebM (melhor compatibilidade)")
                        video_file.unlink()
                        videos_convertidos += 1
                    else:
                        print(f"[INFO] ✓ Vídeo já está em formato compatível")
            
            if videos_convertidos > 0:
                print(f"[INFO] {videos_convertidos} vídeo(s) convertido(s) para WebM")
        except ImportError:
            print("[AVISO] video_converter não disponível, usando vídeos originais")
        except Exception as e:
            print(f"[AVISO] Erro ao converter vídeos: {e}")
        
        # Cria mapeamento dos vídeos para usar no HTML
        for video_file in videos_dest.iterdir():
            if video_file.is_file() and video_file.suffix in ['.mp4', '.avi', '.webm']:
                video_mapping[video_file.name] = f'videos_{timestamp}/{video_file.name}'
        
        print(f"[INFO] Total de vídeos encontrados: {len(video_mapping)}")
        
        # Limpa diretório original após copiar e converter
        for video_file in videos_src.iterdir():
            try:
                if video_file.is_file():
                    video_file.unlink()
            except Exception:
                pass
    
    # Sanitiza nome de cenário/passo como o gerenciador de evidências (para match de arquivos)
    def _sanitizar_nome_arquivo(nome):
        caracteres_proibidos = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        nome_limpo = (nome or '').replace(" ", "_")
        for c in caracteres_proibidos:
            nome_limpo = nome_limpo.replace(c, "_")
        return nome_limpo[:50]

    # Lê o arquivo JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Carrega metadados se disponível
    metadata = {}
    metadata_file = Path('./reports/metadata_temp.json')
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar metadados: {e}")
    
    # Extrai informações dos metadados (compatível com nomes em português e inglês)
    browser_info_raw = metadata.get('navegador', metadata.get('browser', {}))
    system_info_raw = metadata.get('sistema', metadata.get('system', {}))
    test_env_raw = metadata.get('ambiente_teste', metadata.get('test_env', {}))
    execution_info = metadata.get('execucao', metadata.get('execution', {}))
    
    # Mapeia chaves em português para inglês (retrocompatibilidade)
    def obter_valor(dicionario, chave_pt, chave_en, padrao='Unknown'):
        """Tenta pegar valor em português, depois inglês, senão retorna padrão"""
        return dicionario.get(chave_pt, dicionario.get(chave_en, padrao))
    
    # Cria dicionário padronizado para browser_info
    browser_info = {
        'browser': obter_valor(browser_info_raw, 'navegador', 'browser', 'Chrome'),
        'browser_version': obter_valor(browser_info_raw, 'versao_navegador', 'browser_version', 'Unknown'),
        'driver_version': obter_valor(browser_info_raw, 'versao_driver', 'driver_version', 'Unknown'),
        'screen_resolution': obter_valor(browser_info_raw, 'resolucao_tela', 'screen_resolution', 'Unknown'),
        'viewport_size': obter_valor(browser_info_raw, 'tamanho_viewport', 'viewport_size', 'Unknown'),
        'user_agent': obter_valor(browser_info_raw, 'user_agent', 'user_agent', 'Unknown'),
        'platform': obter_valor(browser_info_raw, 'plataforma', 'platform', 'Unknown')
    }
    
    # Cria dicionário padronizado para system_info
    system_info = {
        'os': obter_valor(system_info_raw, 'sistema_operacional', 'os', platform.system()),
        'os_version': obter_valor(system_info_raw, 'versao_sistema', 'os_version', platform.version()),
        'os_release': obter_valor(system_info_raw, 'release_sistema', 'os_release', platform.release()),
        'python_version': obter_valor(system_info_raw, 'versao_python', 'python_version', platform.python_version()),
        'processor': obter_valor(system_info_raw, 'processador', 'processor', platform.processor()),
        'cpu_cores': obter_valor(system_info_raw, 'nucleos_cpu', 'cpu_cores', psutil.cpu_count(logical=False)),
        'cpu_threads': obter_valor(system_info_raw, 'threads_cpu', 'cpu_threads', psutil.cpu_count(logical=True)),
        'ram_total_gb': obter_valor(system_info_raw, 'ram_total_gb', 'ram_total_gb', round(psutil.virtual_memory().total / (1024**3), 2))
    }
    
    # Cria dicionário padronizado para test_env
    test_env = {
        'test_url': obter_valor(test_env_raw, 'url_teste', 'test_url', 'N/A'),
        'timezone': obter_valor(test_env_raw, 'timezone', 'timezone', str(datetime.now().astimezone().tzinfo)),
        'ip_address': obter_valor(test_env_raw, 'endereco_ip', 'ip_address', 'Unknown'),
        'execution_dir': obter_valor(test_env_raw, 'diretorio_execucao', 'execution_dir', str(Path.cwd()))
    }
    
    # Calcula tempo total de execução
    total_duration = 0
    for feature in data:
        for scenario in feature.get('elements', []):
            for step in scenario.get('steps', []):
                duration = step.get('result', {}).get('duration', 0)
                total_duration += duration

    # Formata duração
    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    seconds = int(total_duration % 60)
    duration_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    # Conta estatísticas
    total_features = len(data)
    total_scenarios = sum(len(feature.get('elements', [])) for feature in data)
    
    passed_scenarios = 0
    failed_scenarios = 0
    skipped_scenarios = 0  # NOVO
    undefined_scenarios = 0  # NOVO
    total_steps = 0
    passed_steps = 0
    failed_steps = 0
    skipped_steps = 0
    error_steps = 0
    
    for feature in data:
        for scenario in feature.get('elements', []):
            # Verifica status do cenário diretamente do JSON
            scenario_status = scenario.get('status', 'undefined')
            
            if scenario_status == 'passed':
                passed_scenarios += 1
            elif scenario_status == 'failed':
                failed_scenarios += 1
            elif scenario_status == 'skipped':
                skipped_scenarios += 1
            else:
                undefined_scenarios += 1
            
            for step in scenario.get('steps', []):
                total_steps += 1
                status = step.get('result', {}).get('status', 'undefined')
                if status == 'passed':
                    passed_steps += 1
                elif status == 'failed':
                    failed_steps += 1
                elif status == 'error':
                    error_steps += 1
                elif status == 'skipped':
                    skipped_steps += 1
    
    # Gera HTML
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Testes BDD - Behave</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .header .timestamp {{
            opacity: 0.9;
            font-size: 14px;
        }}
        
        .execution-info {{
            background: white;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .info-header {{
            padding: 15px 30px;
            background: #f8f9fa;
            cursor: pointer;
            user-select: none;
            font-weight: bold;
            font-size: 16px;
            transition: background 0.2s;
        }}
        
        .info-header:hover {{
            background: #e9ecef;
        }}
        
        .info-content {{
            display: none;
            padding: 20px 30px;
        }}
        
        .info-content.expanded {{
            display: block;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .info-section {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
        }}
        
        .info-section h3 {{
            margin-bottom: 15px;
            color: #667eea;
            font-size: 16px;
        }}
        
        .info-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .info-item:last-child {{
            border-bottom: none;
        }}
        
        .info-label {{
            font-weight: 500;
            color: #666;
        }}
        
        .info-value {{
            color: #333;
            font-family: 'Courier New', monospace;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .summary-card .number {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .summary-card .label {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
        }}
        
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .skipped {{ color: #ffc107; }}
        
        .content {{
            padding: 30px;
        }}
        
        .feature {{
            margin-bottom: 30px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .feature-header {{
            background: #667eea;
            color: white;
            padding: 15px 20px;
            font-size: 18px;
            font-weight: bold;
        }}
        
        .feature-description {{
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
            font-style: italic;
            color: #666;
        }}
        
        .scenario {{
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .scenario:last-child {{
            border-bottom: none;
        }}
        
        .scenario-header {{
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
            cursor: pointer;
            user-select: none;
            padding: 10px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}
        
        .scenario-header:hover {{
            background: #f8f9fa;
        }}
        
        .scenario-steps {{
            display: none; /* Colapsado por padrão */
        }}
        
        .scenario-steps.expanded {{
            display: block;
        }}
        
        .toggle-icon {{
            margin-right: 10px;
            transition: transform 0.3s;
            display: inline-block;
        }}
        
        .toggle-icon.expanded {{
            transform: rotate(90deg);
        }}
        
        .filters-section {{
            padding: 20px 30px;
            background: white;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .search-container {{
            margin-bottom: 15px;
        }}
        
        #searchInput {{
            width: 100%;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            transition: border-color 0.3s;
        }}
        
        #searchInput:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .filter-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            color: #666;
        }}
        
        #clearFilters {{
            padding: 8px 16px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }}
        
        #clearFilters:hover {{
            background: #c82333;
        }}
        
        .scenario.hidden {{
            display: none;
        }}
        
        .feature.hidden {{
            display: none;
        }}
        
        .summary-card.clickable {{
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .summary-card.clickable:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .summary-card.clickable:active {{
            transform: translateY(-2px);
        }}
        
        .summary-card.active {{
            border: 3px solid #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}
        
        .step {{
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }}
        
        .step.passed {{
            background: #d4edda;
            border-left: 4px solid #28a745;
        }}
        
        .step.failed {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
        }}
        
        .step.skipped {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
        }}
        
        .step.error {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
        }}
        
        .step-keyword {{
            font-weight: bold;
            margin-right: 8px;
        }}
        
        .step-duration {{
            float: right;
            color: #666;
            font-size: 12px;
        }}
        
        .error-message {{
            background: #f8f9fa;
            border: 1px solid #dc3545;
            border-radius: 4px;
            padding: 15px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #dc3545;
            white-space: pre-wrap;
        }}
        
        .screenshot-container {{
            margin-top: 15px;
            border: 2px solid #dc3545;
            border-radius: 4px;
            padding: 10px;
            background: #f8f9fa;
        }}
        
        .screenshot-title {{
            font-weight: bold;
            color: #dc3545;
            margin-bottom: 10px;
            font-size: 14px;
        }}
        
        .screenshot-image {{
            max-width: 100%;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.2s;
        }}
        
        .screenshot-image:hover {{
            transform: scale(1.02);
        }}
        
        .screenshots-toggle {{
            cursor: pointer;
            padding: 10px 15px;
            background: #e7f3ff;
            border-left: 3px solid #2196F3;
            border-radius: 4px;
            margin-top: 10px;
            user-select: none;
            transition: background 0.2s;
            font-weight: bold;
            font-size: 13px;
        }}
        
        .screenshots-toggle:hover {{
            background: #d0e7ff;
        }}
        
        .screenshots-toggle .toggle-icon {{
            display: inline-block;
            transition: transform 0.3s;
            margin-right: 5px;
        }}
        
        .screenshots-toggle .toggle-icon.expanded {{
            transform: rotate(90deg);
        }}
        
        .screenshots-container {{
            margin-top: 10px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
        }}
        
        .screenshots-controls {{
            padding: 15px 30px;
            background: #fff;
            border-bottom: 2px solid #e0e0e0;
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }}
        
        .screenshots-controls button {{
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: background 0.3s, transform 0.1s;
        }}
        
        .screenshots-controls button:hover {{
            background: #5568d3;
            transform: translateY(-2px);
        }}
        
        .screenshots-controls button:active {{
            transform: translateY(0px);
        }}
        
        .video-container {{
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        
        .video-container h4 {{
            margin: 0 0 15px 0;
            color: #e74c3c;
            font-size: 16px;
            font-weight: bold;
        }}
        
        .video-container video {{
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            background: #000;
        }}
        
        .video-info {{
            margin-top: 10px;
            padding: 10px;
            background: #fff3cd;
            border-left: 3px solid #ffc107;
            border-radius: 4px;
        }}
        
        .video-info small {{
            color: #856404;
        }}
        
        .video-controls-info {{
            margin-top: 10px;
            padding: 8px;
            background: #e7f3ff;
            border-left: 3px solid #2196F3;
            border-radius: 4px;
            text-align: center;
        }}
        
        .video-controls-info a {{
            color: #1976D2;
            text-decoration: none;
            font-weight: bold;
        }}
        
        .video-controls-info a:hover {{
            color: #0D47A1;
            text-decoration: underline;
        }}
        
        /* Modal para visualizar screenshot em tela cheia */
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
        }}
        
        .modal-content {{
            margin: auto;
            display: block;
            max-width: 90%;
            max-height: 90%;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }}
        
        .close-modal {{
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }}
        
        .close-modal:hover {{
            color: #bbb;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Relatório de Testes BDD</h1>
            <div class="timestamp">Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</div>
        </div>
        
        <div class="execution-info">
            <div class="info-header" onclick="toggleInfo(this)">
                <span class="toggle-icon">▶</span>
                Informações de Execução e Ambiente
            </div>
            <div class="info-content">
                <div class="info-grid">
                    <div class="info-section">
                        <h3>Execução</h3>
                        <div class="info-item">
                            <span class="info-label">Duração Total:</span>
                            <span class="info-value">{duration_formatted}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Data/Hora Geração:</span>
                            <span class="info-value">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</span>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3>💻 Sistema</h3>
                        <div class="info-item">
                            <span class="info-label">Sistema Operacional:</span>
                            <span class="info-value">{platform.system()} {platform.release()}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Processador:</span>
                            <span class="info-value">{platform.processor()}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">CPU:</span>
                            <span class="info-value">{psutil.cpu_count(logical=False)} cores / {psutil.cpu_count(logical=True)} threads</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">RAM Total:</span>
                            <span class="info-value">{round(psutil.virtual_memory().total / (1024**3), 2)} GB</span>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3>🌐 Navegador e Ferramentas</h3>
                        <div class="info-item">
                            <span class="info-label">Navegador:</span>
                            <span class="info-value">{browser_info.get('browser', 'Chrome')} {browser_info.get('browser_version', 'Unknown')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">ChromeDriver:</span>
                            <span class="info-value">{browser_info.get('driver_version', 'Unknown')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Resolução Tela:</span>
                            <span class="info-value">{browser_info.get('screen_resolution', 'Unknown')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Viewport:</span>
                            <span class="info-value">{browser_info.get('viewport_size', 'Unknown')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Python:</span>
                            <span class="info-value">{platform.python_version()}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Selenium:</span>
                            <span class="info-value">{selenium.__version__}</span>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3>🔧 Ambiente de Teste</h3>
                        <div class="info-item">
                            <span class="info-label">URL Testada:</span>
                            <span class="info-value">{test_env.get('test_url', 'N/A')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Timezone:</span>
                            <span class="info-value">{test_env.get('timezone', 'Unknown')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">IP Máquina:</span>
                            <span class="info-value">{test_env.get('ip_address', 'Unknown')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Diretório:</span>
                            <span class="info-value" style="font-size: 11px;">{test_env.get('execution_dir', 'Unknown')}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <div class="number">{total_features}</div>
                <div class="label">Features</div>
            </div>
            <div class="summary-card clickable" data-status="passed" onclick="filterByStatus('passed')" title="Clique para filtrar">
                <div class="number passed">{passed_scenarios}</div>
                <div class="label">Cenários Passaram</div>
            </div>
            <div class="summary-card clickable" data-status="failed" onclick="filterByStatus('failed')" title="Clique para filtrar">
                <div class="number failed">{failed_scenarios}</div>
                <div class="label">Cenários Falharam</div>
            </div>
            <div class="summary-card">
                <div class="number passed">{passed_steps}</div>
                <div class="label">Steps Passaram</div>
            </div>
            <div class="summary-card">
                <div class="number failed">{failed_steps}</div>
                <div class="label">Steps Falharam</div>
            </div>
            <div class="summary-card">
                <div class="number failed">{error_steps}</div>
                <div class="label">Steps com Erro</div>
            </div>
            <div class="summary-card">
                <div class="number skipped">{skipped_steps}</div>
                <div class="label">Steps Pulados</div>
            </div>
            <div class="summary-card clickable" data-status="skipped" onclick="filterByStatus('skipped')" title="Clique para filtrar">
                <div class="number skipped">{skipped_scenarios}</div>
                <div class="label">Cenários Pulados</div>
            </div>
            <div class="summary-card clickable" data-status="undefined" onclick="filterByStatus('undefined')" title="Clique para filtrar">
                <div class="number" style="color: #6c757d;">{undefined_scenarios}</div>
                <div class="label">Cenários Não Executados</div>
            </div>
        </div>
        
        <div class="filters-section">
            <div class="search-container">
                <input type="text" 
                       id="searchInput" 
                       placeholder="Buscar cenários ou steps..." 
                       onkeyup="filterScenarios()">
            </div>
            <div class="filter-info">
                <span id="filterStatus">Mostrando todos os cenários</span>
                <button id="clearFilters" onclick="clearAllFilters()" style="display: none;">
                    Limpar Filtros
                </button>
            </div>
        </div>
        
        <div class="screenshots-controls">
            <button onclick="expandAllScreenshots()">▼ Expandir Todas as Evidências</button>
            <button onclick="collapseAllScreenshots()">▲ Colapsar Todas as Evidências</button>
        </div>
        
        <div class="content">
"""
    
    # Adiciona cada feature
    # Contador global de steps (não reseta entre cenários)
    global_step_counter = 0
    
    for feature in data:
        feature_name = feature.get('name', 'Feature sem nome')
        feature_description = feature.get('description', '')
        
        html += f"""
            <div class="feature">
                <div class="feature-header">Funcionalidade: {feature_name}</div>
"""
        
        if feature_description:
            html += f"""
                <div class="feature-description">{feature_description}</div>
"""
        
        # Adiciona cada cenário
        for scenario in feature.get('elements', []):
            scenario_name = scenario.get('name', 'Cenário sem nome')
            scenario_type = scenario.get('type', 'scenario')
            
            if scenario_type == 'background':
                continue  # Pula backgrounds por enquanto
            
            # Determina se cenário falhou
            scenario_failed = any(step.get('result', {}).get('status') in ['failed', 'error'] 
                                for step in scenario.get('steps', []))
            expanded_class = 'expanded' if scenario_failed else ''
            
            html += f"""
                <div class="scenario">
                    <div class="scenario-header" onclick="toggleScenario(this)">
                        <span class="toggle-icon {expanded_class}">▶</span>
                        📋 Cenário: {scenario_name}
                    </div>
                    <div class="scenario-steps {expanded_class}">
"""
            # Nome do cenário sanitizado como no gerenciador de evidências (para vincular screenshots/vídeo ao cenário correto, ex.: Esquema do Cenário @1.1, @1.2, @1.3)
            scenario_name_ascii = unicodedata.normalize('NFKD', scenario_name).encode('ASCII', 'ignore').decode('ASCII')
            scenario_name_sanitized = _sanitizar_nome_arquivo(scenario_name_ascii)
            total_passos_cenario = len(scenario.get('steps', []))
            indice_passo = 0

            # Adiciona cada step (usa contador global)
            for step in scenario.get('steps', []):
                global_step_counter += 1
                indice_passo += 1
                eh_ultimo_passo_cenario = (indice_passo == total_passos_cenario)
                keyword = step.get('keyword', '')
                step_name = step.get('name', '')
                result = step.get('result', {})
                status = result.get('status', 'undefined')
                duration = result.get('duration', 0)
                
                html += f"""
                    <div class="step {status}">
                        <span class="step-keyword">{keyword}</span>
                        <span>{step_name}</span>
                        <span class="step-duration">{duration:.3f}s</span>
                    </div>
"""
                
                # Se falhou ou deu erro, mostra a mensagem de erro
                if status in ['failed', 'error']:
                    error_message = result.get('error_message', 'Erro desconhecido')
                    html += f"""
                    <div class="error-message">{error_message}</div>
"""
                
                # Procura por screenshots deste step vinculados a ESTE cenário (evita misturar evidências de Esquema do Cenário @1.1, @1.2, @1.3)
                # Mantém apenas uma evidência final por teste: em passos que passaram, só mostra screenshot de "ultimo_passo"
                step_screenshots = []
                if screenshot_mapping and scenario_name_sanitized:
                    step_name_sanitized = _sanitizar_nome_arquivo(step_name)
                    for screenshot_file, screenshot_path in screenshot_mapping.items():
                        if not step_name_sanitized or step_name_sanitized not in screenshot_file:
                            continue
                        if scenario_name_sanitized not in screenshot_file:
                            continue
                        if status in ['failed', 'error']:
                            step_screenshots.append(screenshot_path)
                        elif 'ultimo_passo' in screenshot_file and eh_ultimo_passo_cenario:
                            step_screenshots.append(screenshot_path)
                
                # Adiciona screenshots ao HTML (com toggle se não for falha)
                if step_screenshots:
                    if status in ['failed', 'error']:
                        # Para falhas, mostra expandido
                        for screenshot_path in step_screenshots:
                            screenshot_id = screenshot_path.replace('/', '_').replace('.', '_')
                            error_type = "Erro" if status == 'error' else "Falha"
                            html += f"""
                    <div class="screenshot-container">
                        <div class="screenshot-title">📸 Screenshot do {error_type}:</div>
                        <img src="{screenshot_path}" 
                             alt="Screenshot do erro" 
                             class="screenshot-image"
                             onclick="openModal('modal_{screenshot_id}', '{screenshot_path}')">
                    </div>
"""
                    else:
                        # Para passos normais, mostra colapsado
                        html += f"""
                    <div class="screenshots-toggle" onclick="toggleScreenshots(this)">
                        <span class="toggle-icon">▶</span> 📸 {len(step_screenshots)} evidência(s)
                    </div>
                    <div class="screenshots-container" style="display: none;">
"""
                        for screenshot_path in step_screenshots:
                            screenshot_id = screenshot_path.replace('/', '_').replace('.', '_')
                            html += f"""
                        <img src="{screenshot_path}" 
                             alt="Screenshot do passo" 
                             class="screenshot-image"
                             onclick="openModal('modal_{screenshot_id}', '{screenshot_path}')"
                             style="max-width: 100%; margin-bottom: 10px; display: block;">
"""
                        html += """
                    </div>
"""
            
            # Adiciona vídeo se o cenário tiver um associado (usa scenario_name_sanitized já calculado acima)
            scenario_video_file = None
            
            # Procura vídeo que contenha o nome sanitizado do cenário
            for video_file, video_path in video_mapping.items():
                # Extrai apenas o nome do cenário do nome do arquivo (remove timestamp)
                # Formato: video_TIMESTAMP_NOME_CENARIO.mp4
                video_name_parts = video_file.replace('.mp4', '').replace('.avi', '').replace('.webm', '').split('_', 3)
                if len(video_name_parts) >= 4:
                    video_scenario_part = video_name_parts[3]
                    # Compara nomes sanitizados (usa match parcial por causa do limite de 50 chars)
                    if scenario_name_sanitized[:40] in video_scenario_part or video_scenario_part in scenario_name_sanitized:
                        scenario_video_file = video_path
                        break
            
            # Fallback: procura qualquer vídeo que contenha parte do nome
            if not scenario_video_file:
                for video_file, video_path in video_mapping.items():
                    # Tenta match parcial (primeiras 20 caracteres)
                    if len(scenario_name_sanitized) > 15 and scenario_name_sanitized[:20] in video_file:
                        scenario_video_file = video_path
                        break
            
            if scenario_video_file:
                # Determina o status do cenário para mensagem dinâmica
                scenario_status = scenario.get('status', 'undefined')
                scenario_tags = scenario.get('tags', [])
                
                # Gera mensagem dinâmica baseada nas configurações do .env
                video_message = "💡 "
                if env_config.get('GRAVAR_VIDEO_SEMPRE', '').lower() in ('true', 'yes', '1', 'sim'):
                    video_message += "Vídeo gravado em todos os cenários (GRAVAR_VIDEO_SEMPRE=true)"
                elif 'video_always' in scenario_tags:
                    video_message += "Vídeo gravado pela tag @video_always"
                elif scenario_status in ['failed', 'error']:
                    video_message += "Vídeo gravado porque o cenário falhou"
                else:
                    video_message += "Vídeo de evidência capturado"
                
                # Detecta tipo de vídeo pela extensão
                if scenario_video_file.endswith('.webm'):
                    video_type = "video/webm"
                elif scenario_video_file.endswith('.avi'):
                    video_type = "video/x-msvideo"
                else:
                    video_type = "video/mp4"
                
                html += f"""
                    <div class="video-container">
                        <h4>🎥 Vídeo de Evidência</h4>
                        <video controls preload="metadata" width="100%" style="max-width: 900px;">
                            <source src="{scenario_video_file}" type="{video_type}">
                            <source src="{scenario_video_file}" type="video/mp4">
                            <source src="{scenario_video_file}" type="video/webm">
                            <p>Seu navegador não suporta o elemento de vídeo HTML5.</p>
                            <p>Você pode <a href="{scenario_video_file}" download>baixar o vídeo</a> para assistir.</p>
                        </video>
                        <p class="video-info">
                            <small>{video_message}</small>
                        </p>
                        <div class="video-controls-info">
                            <small>
                                🔹 Clique no vídeo para reproduzir | 
                                <a href="{scenario_video_file}" download="evidencia_teste.mp4">💾 Baixar vídeo</a> |
                                <a href="{scenario_video_file}" target="_blank">🔗 Abrir em nova aba</a>
                            </small>
                        </div>
                    </div>
"""
            
            html += """
                    </div>
                </div>
"""
        
        html += """
            </div>
"""
    
    # Fecha HTML
    html += """
        </div>
        
        <div class="footer">
            Relatório gerado automaticamente pelo framework de testes BDD
        </div>
    </div>
    
    <!-- Modal para visualização de screenshots -->
    <div id="screenshotModal" class="modal" onclick="closeModal()">
        <span class="close-modal" onclick="closeModal()">&times;</span>
        <img class="modal-content" id="modalImage">
    </div>
    
    <script>
        function openModal(modalId, imageSrc) {
            var modal = document.getElementById('screenshotModal');
            var modalImg = document.getElementById('modalImage');
            modal.style.display = "block";
            modalImg.src = imageSrc;
            
            // Previne que o clique na imagem feche o modal
            event.stopPropagation();
        }
        
        function closeModal() {
            document.getElementById('screenshotModal').style.display = "none";
        }
        
        // Fecha modal com tecla ESC
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeModal();
            }
        });
        
        // Função para toggle de cenários
        function toggleScenario(header) {
            const stepsDiv = header.nextElementSibling;
            const icon = header.querySelector('.toggle-icon');
            
            stepsDiv.classList.toggle('expanded');
            icon.classList.toggle('expanded');
        }
        
        // Função para toggle de informações
        function toggleInfo(header) {
            const content = header.nextElementSibling;
            const icon = header.querySelector('.toggle-icon');
            
            content.classList.toggle('expanded');
            icon.classList.toggle('expanded');
        }
        
        // Variáveis globais para filtros
        let currentFilter = 'all';
        let currentSearchTerm = '';
        
        // Filtro por texto
        function filterScenarios() {
            currentSearchTerm = document.getElementById('searchInput').value.toLowerCase();
            applyFilters();
        }
        
        // Filtro por status (via cards)
        function filterByStatus(status) {
            // Remove active de todos os cards
            document.querySelectorAll('.summary-card').forEach(card => {
                card.classList.remove('active');
            });
            
            // Se clicar no mesmo filtro, limpa
            if (currentFilter === status) {
                currentFilter = 'all';
            } else {
                currentFilter = status;
                // Adiciona active ao card clicado
                event.currentTarget.classList.add('active');
            }
            
            applyFilters();
        }
        
        // Aplica todos os filtros ativos
        function applyFilters() {
            const features = document.querySelectorAll('.feature');
            let visibleCount = 0;
            
            features.forEach(feature => {
                const scenarios = feature.querySelectorAll('.scenario');
                let featureHasVisible = false;
                
                scenarios.forEach(scenario => {
                    let visible = true;
                    
                    // Filtro por status
                    if (currentFilter !== 'all') {
                        const scenarioStatus = getScenarioStatus(scenario);
                        visible = visible && (scenarioStatus === currentFilter);
                    }
                    
                    // Filtro por texto
                    if (currentSearchTerm) {
                        const scenarioText = scenario.textContent.toLowerCase();
                        visible = visible && scenarioText.includes(currentSearchTerm);
                    }
                    
                    if (visible) {
                        scenario.classList.remove('hidden');
                        featureHasVisible = true;
                        visibleCount++;
                    } else {
                        scenario.classList.add('hidden');
                    }
                });
                
                // Esconde feature se não tem cenários visíveis
                if (featureHasVisible) {
                    feature.classList.remove('hidden');
                } else {
                    feature.classList.add('hidden');
                }
            });
            
            updateFilterStatus(visibleCount);
        }
        
        // Determina status do cenário pelos steps
        function getScenarioStatus(scenario) {
            const steps = scenario.querySelectorAll('.step');
            
            if (steps.length === 0) return 'undefined';
            
            let hasFailed = false;
            let hasError = false;
            let hasSkipped = false;
            let allPassed = true;
            
            steps.forEach(step => {
                if (step.classList.contains('failed')) hasFailed = true;
                if (step.classList.contains('error')) hasError = true;
                if (step.classList.contains('skipped')) hasSkipped = true;
                if (!step.classList.contains('passed')) allPassed = false;
            });
            
            if (hasFailed || hasError) return 'failed';
            if (hasSkipped) return 'skipped';
            if (allPassed) return 'passed';
            return 'undefined';
        }
        
        // Atualiza texto de status do filtro
        function updateFilterStatus(visibleCount) {
            const statusElement = document.getElementById('filterStatus');
            const clearButton = document.getElementById('clearFilters');
            
            const totalScenarios = document.querySelectorAll('.scenario').length;
            
            if (currentFilter !== 'all' || currentSearchTerm) {
                statusElement.textContent = `Mostrando ${visibleCount} de ${totalScenarios} cenários`;
                clearButton.style.display = 'inline-block';
            } else {
                statusElement.textContent = 'Mostrando todos os cenários';
                clearButton.style.display = 'none';
            }
        }
        
        // Limpa todos os filtros
        function clearAllFilters() {
            currentFilter = 'all';
            currentSearchTerm = '';
            document.getElementById('searchInput').value = '';
            
            // Remove active dos cards
            document.querySelectorAll('.summary-card').forEach(card => {
                card.classList.remove('active');
            });
            
            applyFilters();
        }
        
        // Toggle individual de screenshots
        function toggleScreenshots(element) {
            const container = element.nextElementSibling;
            const icon = element.querySelector('.toggle-icon');
            
            if (container.style.display === 'none') {
                container.style.display = 'block';
                icon.classList.add('expanded');
            } else {
                container.style.display = 'none';
                icon.classList.remove('expanded');
            }
        }
        
        // Expandir todos os screenshots
        function expandAllScreenshots() {
            document.querySelectorAll('.screenshots-container').forEach(container => {
                container.style.display = 'block';
            });
            document.querySelectorAll('.screenshots-toggle .toggle-icon').forEach(icon => {
                icon.classList.add('expanded');
            });
        }
        
        // Colapsar todos os screenshots
        function collapseAllScreenshots() {
            document.querySelectorAll('.screenshots-container').forEach(container => {
                container.style.display = 'none';
            });
            document.querySelectorAll('.screenshots-toggle .toggle-icon').forEach(icon => {
                icon.classList.remove('expanded');
            });
        }
    </script>
</body>
</html>
"""
    
    # Salva o arquivo em UTF-8 (utf-8-sig adiciona BOM para melhor reconhecimento no Windows)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8-sig', newline='\n') as f:
        f.write(html)
    
    print(f"\n{'='*60}")
    print(f"[OK] Relatorio HTML gerado com sucesso!")
    print(f"{'='*60}")
    print(f"Localizacao: {output_file}")
    print(f"Estrutura: reports/{year}/{month_name}/{day_folder}/")
    print(f"Timestamp: {timestamp}")
    print(f"{'='*60}\n")
    
    # Abre o relatório automaticamente no navegador padrão
    import webbrowser
    try:
        absolute_path = Path(output_file).resolve()
        webbrowser.open(f'file:///{absolute_path}')
        print(f"[OK] Relatório aberto no navegador padrão")
    except Exception as e:
        print(f"[AVISO] Não foi possível abrir o navegador automaticamente: {e}")
        print(f"[INFO] Abra manualmente: {output_file}")
    
    return str(output_file)

if __name__ == '__main__':
    generate_html_report()


