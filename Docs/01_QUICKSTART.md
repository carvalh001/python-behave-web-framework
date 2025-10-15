# 🚀 Guia de Início Rápido

Este guia vai te ajudar a começar a usar o framework de automação em **5 minutos**.

## ⚡ Passo a Passo

### 1. Ativar Ambiente Virtual

```bash
.\venv\Scripts\activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Criar Arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto e cole este conteúdo:

```env
URL_BASE_SISTEMA=https://sistemacreditogestaowebteste.hml.cloud.poupex
URL_GESTAO_CONTRATOS=https://sistemacreditogestaowebteste.hml.cloud.poupex/contrato
URL_RENEGOCIACAO=https://sistemacreditogestaowebteste.hml.cloud.poupex/renegociacao
URL_API_BASE=https://sistemacreditogestaowebteste.hml.cloud.poupex/api

NAVEGADOR_TIPO=chrome
NAVEGADOR_HEADLESS=false
NAVEGADOR_MAXIMIZAR=true

TIMEOUT_IMPLICITO=10
TIMEOUT_EXPLICITO=10
TIMEOUT_CARREGAMENTO_PAGINA=30

DIRETORIO_RELATORIOS=./reports
DIRETORIO_SCREENSHOTS=./reports/screenshots
DIRETORIO_VIDEOS=./reports/videos

GRAVAR_VIDEO_SEMPRE=false
VIDEO_FPS=15

SCREENSHOT_EM_FALHAS=true
SCREENSHOT_EM_TODOS_PASSOS=false

API_MODO_MOCK=true
API_VERIFICAR_SSL=false

RELATORIO_ABRIR_AUTOMATICAMENTE=true
RELATORIO_ORGANIZAR_POR_DATA=true
```

### 4. Executar Testes

```bash
behave
```

### 5. Visualizar Relatório

O relatório HTML abrirá automaticamente no seu navegador! 🎉

## 📝 Comandos Úteis

### Executar Testes Específicos

```bash
# Apenas testes de quitação
behave --tags=@quitacao

# Apenas testes de renegociação
behave --tags=@renegociacao

# Apenas testes com vídeo
behave --tags=@video_always
```

### Executar com Configuração Diferente

Edite o arquivo `.env` antes de executar:

```env
# Executar sem abrir janela do navegador
NAVEGADOR_HEADLESS=true

# Gravar vídeo de todos os testes
GRAVAR_VIDEO_SEMPRE=true

# Usar API real ao invés de mock
API_MODO_MOCK=false
```

### Gerar Relatório Manualmente

```bash
python generate_report.py
```

## 📂 Estrutura Básica

```
features/
  └── 001_contrato/          # ← Seus cenários de teste (.feature)
      ├── quitacao_contrato.feature
      └── renegociacao_contrato.feature

features/steps/
  ├── 001_contrato_quitacao_steps.py      # ← Implementação dos passos
  └── 001_contrato_renegociacao_steps.py

project_lib/pages/001_contrato/
  ├── 001_gestao_contratos_page.py   # ← Page Objects (telas)
  ├── 002_quitacao_page.py
  └── 003_renegociacao_page.py
```

## 🎯 Criando Seu Primeiro Teste

### 1. Crie um arquivo `.feature`

`features/001_contrato/meu_teste.feature`:

```gherkin
# language: pt
Funcionalidade: Meu Primeiro Teste
  Como usuário
  Eu quero testar algo
  Para garantir que funciona

  Cenário: Exemplo simples
    Dado que eu estou na tela inicial
    Quando eu clico no botão X
    Então vejo a mensagem Y
```

### 2. Implemente os Steps

`features/steps/001_contrato_meu_teste_steps.py`:

```python
from behave import given, when, then

@given('que eu estou na tela inicial')
def acessar_tela_inicial(context):
    context.driver.get("https://seusite.com")

@when('eu clico no botão X')
def clicar_botao_x(context):
    # Use Page Objects para organizar melhor!
    pass

@then('vejo a mensagem Y')
def validar_mensagem_y(context):
    assert "Mensagem" in context.driver.page_source
```

### 3. Execute

```bash
behave features/001_contrato/meu_teste.feature
```

## 🎓 Próximos Passos

1. ✅ Executar os testes de exemplo
2. 📖 Ler o `README.md` completo
3. 🔍 Explorar os Page Objects existentes
4. ✍️ Criar seus próprios cenários de teste

## 💡 Dicas

### 🔥 Atalhos Rápidos

```bash
# Ver ajuda do Behave
behave --help

# Executar sem capturar saída (útil para debug)
behave --no-capture

# Executar com dry-run (não executa, apenas valida)
behave --dry-run

# Parar na primeira falha
behave --stop
```

### 🐛 Debug

Se algo der errado:

1. Verifique se o `.env` existe e está correto
2. Veja os logs no terminal
3. Consulte os screenshots em `reports/screenshots/`
4. Assista os vídeos em `reports/videos/`

### 🏃 Performance

Para testes mais rápidos:

```env
# Executar sem interface gráfica
NAVEGADOR_HEADLESS=true

# Reduzir timeouts (se o sistema for rápido)
TIMEOUT_IMPLICITO=5
TIMEOUT_EXPLICITO=5

# Não gravar vídeos
GRAVAR_VIDEO_SEMPRE=false
```

## ❓ Perguntas Frequentes

### Como adicionar outro navegador?

Edite o `.env`:

```env
NAVEGADOR_TIPO=firefox  # ou edge
```

### Como mudar a URL do sistema?

Edite o `.env`:

```env
URL_BASE_SISTEMA=https://meuambiente.com
```

### Como desabilitar screenshots?

Edite o `.env`:

```env
SCREENSHOT_EM_FALHAS=false
```

## 🆘 Problemas Comuns

### "Module not found"

```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

### "ChromeDriver not found"

O framework baixa automaticamente. Verifique sua internet.

### Vídeos não reproduzem

Consulte `VIDEO_TROUBLESHOOTING.md`

---

**Pronto para começar?** Execute `behave` e veja a mágica acontecer! ✨
