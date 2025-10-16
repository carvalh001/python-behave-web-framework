# Solução: Avisos de Codec OpenH264

## Problema

Durante a execução dos testes com gravação de vídeo, você pode ver mensagens de erro como:

```
Failed to load OpenH264 library: openh264-1.8.0-win64.dll
[libopenh264 @ ...] Incorrect library version loaded
[ERROR:0@0.xxx] global cap_ffmpeg_impl.hpp:3268 open Could not open codec libopenh264
[ERROR:0@0.xxx] global cap_ffmpeg_impl.hpp:3285 open VIDEOIO/FFMPEG: Failed to initialize VideoWriter
```

## **Não se preocupe! Isso é normal e não afeta os testes.**

### O que está acontecendo?

1. O OpenCV tenta usar o codec **OpenH264** para gravar vídeos
2. Esse codec requer uma biblioteca externa (`openh264-1.8.0-win64.dll`) que pode não estar instalada ou estar em versão incompatível
3. O OpenCV **automaticamente usa um codec alternativo** (mp4v ou avc1) que funciona perfeitamente
4. As mensagens são **avisos internos do FFmpeg** (código C++) e aparecem antes do Python poder suprimi-las

### Como foi resolvido?

O arquivo `recursos/utils/gravador_video.py` foi otimizado com:

1. **Variáveis de ambiente** para desabilitar avisos do OpenCV/FFmpeg
2. **Supressão automática de stderr** durante a criação de vídeos
3. **Fallback inteligente de codecs**: o sistema tenta vários codecs na seguinte ordem:
   - `avc1` (H.264 - Melhor para web)
   - `mp4v` (MPEG-4 - Muito compatível) ← **Este geralmente funciona**
   - `H264`, `X264`, `XVID`, `MJPG` (fallbacks adicionais)

### Verificação

Para confirmar que os vídeos estão sendo gravados corretamente:

1. Execute um teste com falha intencional ou com tag `@video_always`
2. Verifique a pasta `reports/videos/`
3. Você deve ver arquivos `.mp4` criados com sucesso

```powershell
Get-ChildItem -Path reports\videos\ | Format-List Name,Length
```

### Mensagens de sucesso esperadas

Quando o vídeo é salvo com sucesso, você verá:

```
[VIDEO] Codec selecionado: mp4v | Frames: 58 | FPS: 15
[VIDEO] Vídeo salvo com sucesso: video_20251016_xxxxxx.mp4
[VIDEO] Mantido (falha detectada): video_20251016_xxxxxx.mp4
```

## Posso eliminar completamente as mensagens de erro?

É **tecnicamente possível** mas não recomendado, pois:

1. As mensagens vêm de código C++ nativo (FFmpeg) que imprime diretamente no console do Windows
2. Suprimi-las completamente requer manipulação de baixo nível do sistema operacional
3. As mensagens são inofensivas e desaparecem rapidamente
4. A solução atual já minimiza as mensagens ao máximo prático

### Se realmente quiser tentar eliminar tudo

Você pode instalar o codec OpenH264 manualmente:

1. Baixe de: https://github.com/cisco/openh264/releases
2. Coloque o arquivo `openh264-1.8.0-win64.dll` em uma das seguintes pastas:
   - `C:\Windows\System32\`
   - Pasta do projeto
   - Pasta do Python/venv

⚠️ **Nota**: Mesmo instalando, pode haver conflitos de versão. A solução atual (usar mp4v) é mais confiável.

## Resumo

✅ **Os vídeos estão sendo gravados com sucesso**  
✅ **As evidências estão funcionando corretamente**  
✅ **O sistema usa automaticamente um codec compatível**  
✅ **Não há impacto nos testes**  

As mensagens de aviso podem ser ignoradas com segurança. 😊

