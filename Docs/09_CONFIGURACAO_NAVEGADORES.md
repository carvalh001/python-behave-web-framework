# Configuração de Navegadores

## Navegadores Suportados

O framework suporta os seguintes navegadores:

### 🟢 **Google Chrome** (Recomendado)
```env
NAVEGADOR_TIPO=chrome
```
- ✅ **Mais estável** e confiável
- ✅ **Melhor suporte** a recursos modernos
- ✅ **Performance superior** em automação
- ✅ **Driver automático** (ChromeDriverManager)
- ✅ **Compatibilidade** com todos os recursos do framework

### 🟡 **Mozilla Firefox**
```env
NAVEGADOR_TIPO=firefox
```
- ✅ **Boa compatibilidade** com padrões web
- ✅ **Open source** e transparente
- ⚠️ **Pode ser mais lento** que Chrome
- ✅ **Driver automático** (GeckoDriverManager)
- ✅ **Suporte completo** a automação

### 🔵 **Microsoft Edge**
```env
NAVEGADOR_TIPO=edge
```
- ✅ **Baseado em Chromium** (mesmo motor do Chrome)
- ✅ **Boa performance** e compatibilidade
- ✅ **Driver automático** (EdgeDriverManager)
- ✅ **Suporte completo** a automação
- ⚠️ **Menos testado** que Chrome/Firefox

## Configurações de Execução

### Modo Headless
```env
# Execução sem interface gráfica (recomendado para CI/CD)
NAVEGADOR_HEADLESS=true

# Execução com interface gráfica (recomendado para debug)
NAVEGADOR_HEADLESS=false
```

**Vantagens do Headless:**
- 🚀 **Execução mais rápida** (sem renderização visual)
- 💾 **Menor uso de memória**
- 🔧 **Ideal para CI/CD** e servidores
- 📊 **Melhor para relatórios** automatizados

### Tamanho da Janela
```env
# Maximizar janela (apenas em modo não-headless)
NAVEGADOR_MAXIMIZAR=true

# Tamanho personalizado
NAVEGADOR_MAXIMIZAR=false
NAVEGADOR_LARGURA=1920
NAVEGADOR_ALTURA=1080
```

**Resoluções Recomendadas:**
- `1920x1080` - Full HD (padrão)
- `1366x768` - HD (notebooks)
- `1280x720` - HD Ready
- `1024x768` - Resolução mínima

## Configurações por Ambiente

### 🏠 **Desenvolvimento Local**
```env
NAVEGADOR_TIPO=chrome
NAVEGADOR_HEADLESS=false
NAVEGADOR_MAXIMIZAR=true
```

### 🏢 **CI/CD / Servidor**
```env
NAVEGADOR_TIPO=chrome
NAVEGADOR_HEADLESS=true
NAVEGADOR_LARGURA=1920
NAVEGADOR_ALTURA=1080
```

### 🐛 **Debug / Troubleshooting**
```env
NAVEGADOR_TIPO=chrome
NAVEGADOR_HEADLESS=false
NAVEGADOR_MAXIMIZAR=true
PAUSAR_EM_ERRO=true
```

## Solução de Problemas

### Chrome
- **Driver não encontrado**: O ChromeDriverManager baixa automaticamente
- **Versão incompatível**: Atualize o Chrome para a versão mais recente
- **Permissões**: Certifique-se de que o Chrome pode ser executado

### Firefox
- **GeckoDriver**: Baixado automaticamente pelo GeckoDriverManager
- **Perfis**: O framework cria um perfil temporário limpo
- **Performance**: Pode ser mais lento que Chrome em alguns casos

### Edge
- **Windows**: Funciona melhor no Windows 10/11
- **Driver**: EdgeDriverManager gerencia automaticamente
- **Compatibilidade**: Mesmo motor do Chrome, boa compatibilidade

## Exemplo Completo

```env
# ============================================================
# CONFIGURACOES DO NAVEGADOR
# ============================================================
# Opcoes disponiveis: chrome, firefox, edge
# chrome: Google Chrome (mais estavel, melhor suporte a recursos)
# firefox: Mozilla Firefox (boa compatibilidade, pode ser mais lento)
# edge: Microsoft Edge (baseado em Chromium, boa performance)
NAVEGADOR_TIPO=chrome

# Executa o navegador sem interface grafica (mais rapido, ideal para CI/CD)
# true: Modo headless (sem janela visivel)
# false: Modo normal (com janela visivel)
NAVEGADOR_HEADLESS=true

# Maximiza a janela do navegador ao iniciar (apenas em modo nao-headless)
# true: Maximiza a janela
# false: Usa tamanho personalizado (NAVEGADOR_LARGURA x NAVEGADOR_ALTURA)
NAVEGADOR_MAXIMIZAR=true

# Tamanho da janela do navegador (quando NAVEGADOR_MAXIMIZAR=false)
# Valores recomendados: 1920x1080, 1366x768, 1280x720
NAVEGADOR_LARGURA=1920
NAVEGADOR_ALTURA=1080
```

## Dicas de Performance

1. **Use Chrome** para melhor performance
2. **Headless=true** para execução mais rápida
3. **Resolução adequada** (1920x1080 é ideal)
4. **Evite maximizar** em headless (use tamanho fixo)
5. **Monitore memória** em execuções longas

## Suporte a Recursos

| Recurso | Chrome | Firefox | Edge |
|---------|--------|---------|------|
| Screenshots | ✅ | ✅ | ✅ |
| Vídeos | ✅ | ✅ | ✅ |
| Headless | ✅ | ✅ | ✅ |
| Mobile Emulation | ✅ | ⚠️ | ✅ |
| DevTools | ✅ | ✅ | ✅ |
| Performance | 🟢 | 🟡 | 🟢 |
