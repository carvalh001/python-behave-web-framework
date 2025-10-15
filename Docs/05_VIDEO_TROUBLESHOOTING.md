# 🎥 Troubleshooting - Vídeos no Relatório HTML

## ✅ Status Atual

O sistema está gravando vídeos com codec **H.264** que é totalmente compatível com navegadores modernos.

## 🔍 Como Verificar se o Vídeo Está Funcionando

### 1. Abrir o Relatório HTML
```
reports/2025/10/15/report_TIMESTAMP.html
```

### 2. Localizar o Vídeo
- Procure pela seção **"🎥 Vídeo de Evidência"**
- Deve haver um player de vídeo com controles
- Três opções abaixo do vídeo:
  - 📹 Clique no vídeo para reproduzir
  - 💾 Baixar vídeo
  - 🔗 Abrir em nova aba

### 3. Testar Reprodução
Clique no botão **Play** (▶️) no player de vídeo

## 🐛 Problemas Comuns e Soluções

### Problema 1: Vídeo Não Reproduz (Tela Preta)

**Causas Possíveis:**
- Codec não suportado pelo navegador
- Arquivo de vídeo corrompido
- Caminho relativo incorreto

**Soluções:**

1. **Verificar codec do vídeo:**
```bash
# No terminal (com venv ativado)
python -c "import cv2; cap = cv2.VideoCapture('reports/videos/VIDEO.mp4'); print('FourCC:', int(cap.get(cv2.CAP_PROP_FOURCC))); cap.release()"
```

2. **Baixar e reproduzir diretamente:**
- Clique em "💾 Baixar vídeo"
- Abra o arquivo baixado no VLC ou Windows Media Player
- Se reproduzir, o problema é de compatibilidade do navegador

3. **Abrir em nova aba:**
- Clique em "🔗 Abrir em nova aba"
- Se reproduzir, o problema é de embedding no HTML

### Problema 2: Player Aparece mas Mostra Erro

**Causas:**
- Tipo MIME incorreto
- Arquivo de vídeo vazio

**Soluções:**

1. **Verificar tamanho do arquivo:**
```bash
# PowerShell
Get-Item reports\videos\*.mp4 | Select-Object Name, Length
```

Se o arquivo tiver 0 bytes ou < 100KB, o vídeo não foi gravado corretamente.

2. **Regenerar vídeo:**
```bash
# Limpar vídeos antigos
Remove-Item reports\videos\* -Force

# Executar teste novamente
behave features/TESTE.feature --tags=@video_always
```

### Problema 3: Vídeo Muito Lento ou Travado

**Causas:**
- FPS muito baixo (< 10)
- Resolução muito alta

**Soluções:**

1. **Ajustar FPS (em environment.py):**
```python
context.video_recorder = VideoRecorder(video_path, driver=context.driver, fps=20)  # Era 15
```

2. **Reduzir resolução da janela:**
```python
# No before_scenario
context.driver.set_window_size(1280, 720)  # Em vez de maximize_window()
```

### Problema 4: Timestamp Não Aparece no Vídeo

**Causas:**
- Erro no overlay de texto
- Fonte não disponível no sistema

**Soluções:**
O timestamp usa fonte padrão do OpenCV (FONT_HERSHEY_SIMPLEX), sempre disponível.

Se não aparecer, verifique se os frames estão sendo capturados:
```python
# Adicionar print no video_recorder.py
print(f"Frames capturados: {len(self.frames)}")
```

### Problema 5: Vídeo Grava Tela Inteira em Vez da Janela

**Causas:**
- `driver.get_window_rect()` falha
- Fallback para tela inteira ativado

**Soluções:**

1. **Verificar logs:**
Procure por:
```
[VIDEO] Janela do navegador: WIDTHxHEIGHT
```

Se não aparecer, o driver não conseguiu obter dimensões da janela.

2. **Forçar dimensões específicas:**
```python
# No environment.py, antes de iniciar gravação
context.driver.set_window_size(1280, 720)
context.driver.set_window_position(0, 0)
```

## 🔧 Conversão Manual para WebM

Se o vídeo MP4 não reproduzir em navegador algum:

```python
from project_lib.utils.video_converter import convert_to_webm

# Converter vídeo manualmente
input_video = "reports/videos/video.mp4"
output_video = convert_to_webm(input_video)
print(f"Vídeo convertido: {output_video}")
```

## 📊 Verificação de Compatibilidade

### Navegadores Testados:

| Navegador | H.264/MP4 | WebM/VP9 | Status |
|-----------|-----------|----------|--------|
| Chrome    | ✅        | ✅       | OK     |
| Edge      | ✅        | ✅       | OK     |
| Firefox   | ✅        | ✅       | OK     |
| Safari    | ✅        | ❌       | OK (MP4 apenas) |
| IE11      | ⚠️        | ❌       | Parcial |

### Codecs Suportados:

1. **H.264 (melhor)** ✅
   - Suporte universal
   - Boa compressão
   - Hardware acceleration

2. **WebM/VP9** ✅
   - Suporte moderno
   - Melhor compressão que H.264
   - Open source

3. **MP4V** ⚠️
   - Suporte limitado
   - Pode não funcionar em alguns navegadores
   - Sistema tenta evitar

## 🎯 Alternativas ao Player Embutido

### Opção 1: Abrir em Nova Aba
```html
<!-- Já implementado -->
<a href="video.mp4" target="_blank">Abrir vídeo</a>
```

### Opção 2: Link para Download
```html
<!-- Já implementado -->
<a href="video.mp4" download>Baixar vídeo</a>
```

### Opção 3: Usar Player Externo (VLC, etc)
1. Baixar vídeo do relatório
2. Abrir com VLC Media Player
3. Funciona com qualquer codec

## 📝 Logs Úteis

Durante execução do teste, procure por:

```
[VIDEO] Gravação iniciada: video_TIMESTAMP.mp4
[VIDEO] Janela do navegador: 1920x1080
[VIDEO] Usando codec: avc1  (ou H264, X264, etc)
[VIDEO] Vídeo salvo com sucesso: video.mp4 (XXX frames)
```

Durante geração do relatório:

```
[OK] Vídeos copiados para: reports/2025/10/15/videos_TIMESTAMP
[CONVERTER] Vídeo atual usa codec: h264
[CONVERTER] Codec h264 é web-compatível
[INFO] Total de vídeos encontrados: 1
```

## 🆘 Última Recurso

Se nada funcionar, use FFmpeg para converter manualmente:

```bash
# Instalar FFmpeg (Windows)
choco install ffmpeg

# Converter vídeo
ffmpeg -i input.mp4 -c:v libx264 -preset fast -crf 23 output.mp4

# Ou para WebM
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 output.webm
```

## ✅ Checklist de Verificação

- [ ] Vídeo foi criado em `reports/videos/`
- [ ] Vídeo tem tamanho > 100KB
- [ ] Vídeo reproduz no VLC/Windows Media Player
- [ ] Codec é H.264 ou WebM
- [ ] Vídeo foi copiado para pasta do relatório
- [ ] HTML possui tag `<video>` com src correto
- [ ] Navegador é moderno (Chrome/Edge/Firefox)
- [ ] Caminho relativo do vídeo está correto

## 📧 Suporte

Se o problema persistir:
1. Verifique todos itens do checklist
2. Cole os logs completos (console output)
3. Informe navegador e versão
4. Anexe o arquivo de vídeo para análise

