# Melhorias em Evidências e Relatórios

## Resumo das Implementações

Este documento descreve as melhorias implementadas no sistema de evidências (screenshots e vídeos) e no relatório HTML.

---

## 1. Screenshots em Todos os Passos

### Implementação

Agora é possível capturar screenshots de **todos os passos** de um cenário, não apenas os que falharam.

### Configuração

```env
SCREENSHOT_EM_TODOS_PASSOS=true
```

### Comportamento

- Captura screenshot de cada passo do cenário
- Usa nomenclatura: `passo_{indice}_{timestamp}_{nome_passo}.png`
- Não duplica screenshots de passos que falharam
- Exibido no relatório HTML com toggle colapsável

### Exemplo de Saída

```
[SCREENSHOT] Passo 1 capturado: passo_1_20251016_155643_468365_que_eu_estou_na_tela_de_Renegociacao.png
[SCREENSHOT] Passo 2 capturado: passo_2_20251016_155643_762038_eu_preencho_o_CPF_no_filtro.png
...
```

---

## 2. Relatório HTML Aprimorado

### Screenshots Colapsáveis

Todos os screenshots agora são exibidos no relatório com controle de visibilidade:

- **Passos com falha**: Screenshots expandidos por padrão
- **Passos normais**: Screenshots colapsados, clique para expandir
- **Contador visual**: Mostra quantos screenshots cada passo possui

### Botões de Controle Global

Adicionados dois botões no topo do relatório:

- **▼ Expandir Todas as Evidências**: Mostra todos os screenshots de uma vez
- **▲ Colapsar Todas as Evidências**: Oculta todos os screenshots

### Interface

```html
<div class="screenshots-toggle" onclick="toggleScreenshots(this)">
    <span class="toggle-icon">▶</span> 📸 3 evidência(s)
</div>
<div class="screenshots-container" style="display: none;">
    <!-- Screenshots aqui -->
</div>
```

---

## 3. Mensagens Dinâmicas de Evidências

### Vídeos

As mensagens de vídeo agora refletem a configuração do `.env`:

| Configuração | Mensagem Exibida |
|--------------|------------------|
| `GRAVAR_VIDEO_SEMPRE=true` | "Vídeo gravado em todos os cenários (GRAVAR_VIDEO_SEMPRE=true)" |
| Tag `@video_always` | "Vídeo gravado pela tag @video_always" |
| Cenário falhou | "Vídeo gravado porque o cenário falhou" |
| Outro motivo | "Vídeo de evidência capturado" |

### Screenshots

Mensagens contextuais baseadas na configuração:

| Configuração | Descrição |
|--------------|-----------|
| `SCREENSHOT_EM_TODOS_PASSOS=true` | Screenshots em todos os passos |
| `SCREENSHOT_ULTIMO_PASSO=true` | Screenshot apenas do último passo |
| `SCREENSHOT_EM_FALHAS=true` | Screenshots apenas em falhas |

---

## 4. Correção de Reprodução de Vídeos

### Problema Identificado

Os vídeos eram gravados com codec **FMP4** (MP4 Fragmentado), que não é bem suportado em navegadores HTML5.

### Solução Implementada

1. **Conversão Automática**: Vídeos com codecs problemáticos (FMP4, MP4V) são automaticamente convertidos para WebM (VP9/VP8)
2. **Melhor Compatibilidade**: WebM é nativamente suportado por Chrome, Firefox, Edge
3. **Supressão de Avisos**: Mensagens técnicas do FFmpeg foram suprimidas

### Tags HTML Melhoradas

```html
<video controls preload="metadata" width="100%">
    <source src="video.webm" type="video/webm">
    <source src="video.mp4" type="video/mp4">
    <!-- Fallback com link de download -->
</video>
```

### Processo de Conversão

```
[INFO] Verificando compatibilidade: video_xxx.mp4
[CONVERTER] Vídeo atual usa codec: FMP4
[CONVERTER] Codec FMP4 pode ter problemas de compatibilidade
[CONVERTER] Tentando converter para WebM...
[CONVERTER] Usando codec WebM: VP90
[CONVERTER] Conversão concluída: video_xxx.webm
[INFO] ✓ Vídeo convertido para WebM (melhor compatibilidade)
```

---

## 5. Três Modos de Captura de Screenshots

### Comparação Completa

| Modo | Variável | Quando | Quantidade | Uso Ideal |
|------|----------|--------|------------|-----------|
| **Em Falhas** | `SCREENSHOT_EM_FALHAS=true` | Passos que falharam | Baixa | Debugging |
| **Todos os Passos** | `SCREENSHOT_EM_TODOS_PASSOS=true` | Cada passo | Alta | Auditoria completa |
| **Último Passo** | `SCREENSHOT_ULTIMO_PASSO=true` | Último passo do cenário | Média | Evidência final |

### Configurações Recomendadas

#### Para Debugging
```env
SCREENSHOT_EM_FALHAS=true
SCREENSHOT_EM_TODOS_PASSOS=false
SCREENSHOT_ULTIMO_PASSO=false
GRAVAR_VIDEO_SEMPRE=false
```

#### Para Auditoria Completa
```env
SCREENSHOT_EM_FALHAS=true
SCREENSHOT_EM_TODOS_PASSOS=true
SCREENSHOT_ULTIMO_PASSO=false
GRAVAR_VIDEO_SEMPRE=true
```

#### Balanceado (Recomendado)
```env
SCREENSHOT_EM_FALHAS=true
SCREENSHOT_EM_TODOS_PASSOS=false
SCREENSHOT_ULTIMO_PASSO=true
GRAVAR_VIDEO_SEMPRE=false
```

---

## 6. Melhorias de Performance

### Conversão Inteligente

- Apenas vídeos com codecs problemáticos são convertidos
- Vídeos já compatíveis (H.264) são mantidos
- Progresso da conversão exibido em tempo real

### Supressão de Avisos

- Avisos técnicos do FFmpeg/OpenCV foram suprimidos
- Console mais limpo e profissional
- Apenas mensagens relevantes são exibidas

---

## Exemplo de Uso Completo

### 1. Configure o .env

```env
SCREENSHOT_EM_TODOS_PASSOS=true
SCREENSHOT_ULTIMO_PASSO=false
GRAVAR_VIDEO_SEMPRE=false
```

### 2. Execute os testes

```bash
behave
```

### 3. Gere o relatório

```bash
python generate_report.py
```

### 4. Verifique o resultado

- Relatório abre automaticamente no navegador
- Screenshots de todos os passos aparecem colapsados
- Clique em "▼ Expandir Todas as Evidências" para ver todos
- Vídeos reproduzem diretamente no navegador (formato WebM)
- Mensagens dinâmicas explicam por que cada evidência foi capturada

---

## Arquivos Modificados

1. `features/environment.py` - Lógica de captura de screenshots
2. `recursos/utils/gerenciador_evidencias.py` - Métodos de captura
3. `recursos/utils/gerenciador_configuracao.py` - Propriedade `screenshot_ultimo_passo`
4. `recursos/utils/video_converter.py` - Supressão de avisos
5. `generate_report.py` - Renderização de evidências, mensagens dinâmicas, controles
6. `env.example` - Documentação de configurações

---

## Benefícios

- Flexibilidade total no nível de evidências
- Relatórios mais informativos e interativos
- Vídeos reproduzem corretamente em todos os navegadores
- Mensagens contextuais baseadas nas configurações
- Interface amigável com controles de expansão/colapso
- Performance otimizada com conversão inteligente

---

**Versão**: 1.2.0  
**Data**: 16/10/2025  
**Autor**: Framework de Automação Siepex

