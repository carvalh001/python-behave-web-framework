#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Conversor de Vídeo para WebM
Converte vídeos MP4 problemáticos para WebM (melhor compatibilidade web)
"""
import os
import sys

# Suprime avisos do OpenCV durante conversões
os.environ['OPENCV_LOG_LEVEL'] = 'SILENT'
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'

import cv2
from pathlib import Path

# Desabilita logs do OpenCV
cv2.setLogLevel(0)


def convert_to_webm(input_path, output_path=None):
    """
    Converte um vídeo para formato WebM (VP8/VP9)
    
    Args:
        input_path (str): Caminho do vídeo de entrada
        output_path (str, optional): Caminho do vídeo de saída. 
                                     Se None, usa mesmo nome com extensão .webm
    
    Returns:
        str: Caminho do arquivo convertido, ou None se falhar
    """
    try:
        input_path = Path(input_path)
        
        if output_path is None:
            output_path = input_path.with_suffix('.webm')
        else:
            output_path = Path(output_path)
        
        # Abre o vídeo de entrada
        cap = cv2.VideoCapture(str(input_path))
        
        if not cap.isOpened():
            print(f"[CONVERTER] Erro ao abrir vídeo: {input_path}")
            return None
        
        # Obtém propriedades do vídeo
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"[CONVERTER] Convertendo {input_path.name}")
        print(f"[CONVERTER] Resolução: {width}x{height}, FPS: {fps}, Frames: {frame_count}")
        
        # Tenta usar VP9 (melhor), depois VP80 (fallback)
        fourcc_options = [
            'VP90',  # VP9 - Melhor qualidade/compressão
            'VP80',  # VP8 - Mais compatível
        ]
        
        # Suprime stderr para evitar avisos do FFmpeg
        stderr_backup = None
        devnull = None
        try:
            stderr_fd = sys.stderr.fileno()
            stderr_backup = os.dup(stderr_fd)
            devnull = os.open(os.devnull, os.O_WRONLY)
            sys.stderr.flush()
            os.dup2(devnull, stderr_fd)
        except (AttributeError, OSError):
            pass  # Se falhar, continua sem supressão
        
        try:
            out = None
            codec_usado = None
            for fourcc_str in fourcc_options:
                try:
                    fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
                    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
                    
                    if out.isOpened():
                        codec_usado = fourcc_str
                        break
                    else:
                        out.release()
                        out = None
                except Exception:
                    if out:
                        out.release()
                    out = None
        finally:
            # Restaura stderr
            if stderr_backup is not None and devnull is not None:
                try:
                    sys.stderr.flush()
                    os.dup2(stderr_backup, sys.stderr.fileno())
                    os.close(stderr_backup)
                    os.close(devnull)
                except (OSError, ValueError):
                    pass
        
        if codec_usado:
            print(f"[CONVERTER] Usando codec WebM: {codec_usado}")
        
        if out is None or not out.isOpened():
            print("[CONVERTER] Nenhum codec WebM disponível")
            cap.release()
            return None
        
        # Converte frame por frame
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            out.write(frame)
            frame_idx += 1
            
            # Mostra progresso a cada 30 frames
            if frame_idx % 30 == 0:
                progress = (frame_idx / frame_count) * 100 if frame_count > 0 else 0
                print(f"[CONVERTER] Progresso: {progress:.1f}%", end='\r')
        
        # Libera recursos
        cap.release()
        out.release()
        
        print(f"\n[CONVERTER] Conversão concluída: {output_path.name}")
        return str(output_path)
        
    except Exception as e:
        print(f"[CONVERTER] Erro na conversão: {e}")
        return None


def ensure_web_compatible_video(video_path):
    """
    Garante que o vídeo seja compatível com navegadores web.
    Se for MP4V, tenta converter para WebM.
    
    Args:
        video_path (str): Caminho do vídeo
    
    Returns:
        str: Caminho do vídeo compatível (original ou convertido)
    """
    try:
        video_path = Path(video_path)
        
        if not video_path.exists():
            return str(video_path)
        
        # Verifica codec do vídeo
        cap = cv2.VideoCapture(str(video_path))
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        cap.release()
        
        # Converte fourcc para string
        fourcc_str = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
        
        print(f"[CONVERTER] Vídeo atual usa codec: {fourcc_str}")
        
        # Codecs nativos e compatíveis com navegadores (não precisam conversão)
        compatible_codecs = ['avc1', 'AVC1', 'h264', 'H264', 'MJPG', 'mjpg']
        
        # Codecs problemáticos que precisam conversão
        problematic_codecs = ['mp4v', 'MP4V', 'FMP4']
        
        # Verifica se é compatível
        if fourcc_str in compatible_codecs:
            print(f"[CONVERTER] Codec {fourcc_str} é compatível com navegadores (sem conversão necessária)")
            return str(video_path)
        
        if fourcc_str in problematic_codecs:
            print(f"[CONVERTER] Codec {fourcc_str} pode ter problemas de compatibilidade")
            print(f"[CONVERTER] Tentando converter para WebM...")
            
            webm_path = convert_to_webm(video_path)
            
            if webm_path and Path(webm_path).exists():
                print(f"[CONVERTER] Usando vídeo WebM convertido")
                return webm_path
            else:
                print(f"[CONVERTER] Conversão falhou, usando vídeo original")
                return str(video_path)
        else:
            print(f"[CONVERTER] Codec {fourcc_str} é web-compatível")
            return str(video_path)
            
    except Exception as e:
        print(f"[CONVERTER] Erro ao verificar compatibilidade: {e}")
        return str(video_path)

