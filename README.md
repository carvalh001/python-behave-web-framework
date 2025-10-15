# Framework de Automação de Testes Web - Siepex

Framework de automação de testes frontend web orientado a comportamento (BDD), projetado para ser fácil de manter.

## 🎓 Nunca Programou? Comece Aqui!

Se você **nunca programou em Python** ou **nunca fez automação web**, temos tutoriais completos para você:

👉 **[00 Instruções/](00%20Instruções/README.md)** - Tutorial completo do zero!

Aprenda:
- Fundamentos de Python (variáveis, listas, métodos, classes)
- Automação Web com Selenium (os 4 pilares)
- Como integrar tudo no framework BDD
- Exercícios práticos passo a passo

**Tempo**: 7-10 horas | **Nível**: Iniciante absoluto

---

## 🎯 Características

- **100% em Português**: Código, variáveis, métodos e documentação em português
- **Estrutura Numerada**: Pastas e arquivos numerados (001_, 002_) para facilitar navegação
- **Auto-explicativo**: Nomes descritivos que contam uma história
- **BDD com Behave**: Cenários escritos em Gherkin (português)
- **Configuração Centralizada**: Todas as configurações no arquivo `.env`
- **Gerenciadores Especializados**: Abstrações que simplificam a complexidade
- **Evidências Automáticas**: Screenshots em falhas e vídeos opcionais
- **Relatórios HTML**: Relatórios visuais e interativos

## 📁 Estrutura do Projeto

```
Siepex/
├── README.md                         ⭐ COMECE AQUI
├── .env                              🔧 Configurações
│
├── 00 Instruções/                    🎓 Tutoriais Python do zero
│   └── ... (7 tutoriais)
│
├── Docs/                             📚 Documentação do framework
│   └── ... (10 documentos)
│
├── features/                         🎭 Testes BDD
│   ├── contrato/                         (Sistema)
│   ├── exemplos/                         ⭐ (ServeRest)
│   ├── steps/
│   └── environment.py
│
├── pages/                            📄 Page Objects (RAIZ!)
│   ├── base_page.py                      (PaginaBase)
│   ├── contrato/                         (Sistema)
│   └── exemplos/                         ⭐ (ServeRest)
│
├── recursos/                         🔧 Infraestrutura
│   ├── apis/                             (Antes services)
│   │   └── contrato_service.py
│   └── utils/                            (Gerenciadores)
│       ├── auxiliar_datas.py
│       ├── gerenciador_configuracao.py
│       ├── gerenciador_navegador.py
│       ├── gerenciador_evidencias.py
│       └── gerenciador_relatorio.py
│
└── reports/                          📊 Relatórios
```

> 💡 **Estrutura detalhada**: **[Docs/00_ESTRUTURA_PROJETO.md](Docs/00_ESTRUTURA_PROJETO.md)**

## 🚀 Configuração Inicial

### 1. Instalar Dependências

```bash
# Ativar ambiente virtual (recomendado)
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Criar Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# URLs DO SISTEMA
URL_BASE_SISTEMA=https://sistemacreditogestaowebteste.hml.cloud.poupex
URL_GESTAO_CONTRATOS=https://sistemacreditogestaowebteste.hml.cloud.poupex/contrato
URL_RENEGOCIACAO=https://sistemacreditogestaowebteste.hml.cloud.poupex/renegociacao
URL_API_BASE=https://sistemacreditogestaowebteste.hml.cloud.poupex/api

# NAVEGADOR
NAVEGADOR_TIPO=chrome
NAVEGADOR_HEADLESS=false
NAVEGADOR_MAXIMIZAR=true

# TIMEOUTS (em segundos)
TIMEOUT_IMPLICITO=10
TIMEOUT_EXPLICITO=10
TIMEOUT_CARREGAMENTO_PAGINA=30

# DIRETÓRIOS
DIRETORIO_RELATORIOS=./reports
DIRETORIO_SCREENSHOTS=./reports/screenshots
DIRETORIO_VIDEOS=./reports/videos

# VÍDEO
GRAVAR_VIDEO_SEMPRE=false
VIDEO_FPS=15

# SCREENSHOTS
SCREENSHOT_EM_FALHAS=true
SCREENSHOT_EM_TODOS_PASSOS=false

# API
API_MODO_MOCK=true
API_VERIFICAR_SSL=false

# RELATÓRIOS
RELATORIO_ABRIR_AUTOMATICAMENTE=true
RELATORIO_ORGANIZAR_POR_DATA=true
```

## ▶️ Executando os Testes

### Executar Todos os Testes

```bash
behave
```

### Executar por Tags

```bash
# Apenas testes de quitação
behave --tags=@quitacao

# Apenas testes de renegociação
behave --tags=@renegociacao

# Testes regressivos
behave --tags=@regressivo
```

### Gerar Relatório HTML

```bash
# Os testes já geram relatório automaticamente
# Ou execute manualmente:
python generate_report.py
```

## 📝 Como Adicionar Novos Testes

### 1. Criar Feature (Cenário)

Arquivo: `features/001_contrato/novo_teste.feature`

```gherkin
# language: pt
Funcionalidade: Nome da Funcionalidade
  Descrição do que será testado

  Cenário: Nome do Cenário
    Dado que estou na tela X
    Quando eu faço a ação Y
    Então o resultado Z é exibido
```

### 2. Criar Steps (Passos)

Arquivo: `features/steps/001_contrato_novo_steps.py`

```python
from behave import given, when, then

@given('que estou na tela X')
def acessar_tela_x(context):
    """Navega para a tela X"""
    # Implementação
    pass
```

### 3. Criar Page Object (se necessário)

Arquivo: `project_lib/pages/001_contrato/004_nova_page.py`

```python
from project_lib.pages.base_page import PaginaBase
from selenium.webdriver.common.by import By

class PaginaNova(PaginaBase):
    """Página Nova"""
    
    _BOTAO_EXEMPLO = (By.ID, "btnExemplo")
    
    def __init__(self, driver, configuracao=None):
        super().__init__(driver)
        self.configuracao = configuracao
    
    def clicar_botao_exemplo(self):
        """Clica no botão exemplo"""
        self.clicar_no_elemento(self._BOTAO_EXEMPLO)
```

## 🎓 Guia para Iniciantes

### Conceitos Importantes

1. **Feature**: Arquivo `.feature` que descreve o comportamento esperado em linguagem natural
2. **Step**: Função Python que implementa cada linha do cenário
3. **Page Object**: Classe que representa uma página web e suas ações
4. **Localizador**: Tupla que identifica elementos na página (ex: `(By.ID, "nome")`)

### Padrão de Nomenclatura

- **Métodos de ação**: `clicar_botao_X()`, `preencher_campo_Y()`
- **Métodos de validação**: `validar_X()`, `verificar_Y()`
- **Métodos de obtenção**: `obter_texto_X()`, `obter_valor_Y()`
- **Localizadores**: `_BOTAO_X`, `_CAMPO_INPUT_Y`, `_TABELA_Z`

### Onde Mexer

Como analista/testador, você trabalhará principalmente em:

1. **features/001_X/**: Escrever cenários de teste
2. **features/steps/001_X_steps.py**: Implementar os passos
3. **project_lib/pages/001_X/**: Criar/atualizar Page Objects

Evite modificar:
- `environment.py` (gerenciado automaticamente)
- `recursos/` (infraestrutura - gerenciadores e utils)
- `behave.ini` (configuração do framework)

Para aprender, use:
- `features/exemplos/` - Testes práticos ServeRest
- `pages/exemplos/` - Page Objects didáticos

## 🔧 Configurações Avançadas

### Modo Headless

Para executar sem interface gráfica:

```env
NAVEGADOR_HEADLESS=true
```

### Gravar Todos os Vídeos

Para gravar vídeo de todos os cenários (não apenas falhas):

```env
GRAVAR_VIDEO_SEMPRE=true
```

### Usar API Real (ao invés de Mock)

```env
API_MODO_MOCK=false
```

## 📊 Relatórios

Os relatórios são gerados automaticamente em:

```
reports/
  └── 2025/
      └── Outubro/
          └── Testes - 2025-10-15 16h33/
              ├── report_15-10-2025_16-33.html
              ├── results_15-10-2025_16-33.json
              ├── screenshots_15-10-2025_16-33/
              └── videos_15-10-2025_16-33/
```

### Recursos do Relatório

- ✅ Filtragem por status (passou/falhou)
- 🔍 Busca por texto
- 📸 Screenshots automáticos em falhas
- 🎥 Vídeos de evidência
- 📊 Estatísticas de execução
- 💻 Informações de ambiente

## 🐛 Troubleshooting

### Erro: "Elemento não encontrado"

- Verifique se o localizador está correto
- Aumente o `TIMEOUT_IMPLICITO` no `.env`
- Use `aguardar_texto_aparecer=True` em `obter_texto_do_elemento()`

### Erro: "ChromeDriver não encontrado"

- O `webdriver-manager` baixa automaticamente
- Verifique sua conexão com a internet

### Vídeos não são reproduzidos no relatório

- Consulte `VIDEO_TROUBLESHOOTING.md`
- Tente converter para formato WebM

## 📚 Documentação Completa

### 🎓 Para Iniciantes em Programação

**[00 Instruções/](00%20Instruções/README.md)** - Tutorial Python e Automação Web do ZERO

Aprenda passo a passo:
1. Fundamentos de Python (variáveis, listas, loops)
2. Orientação a Objetos (métodos, classes, herança)
3. Automação Web (os 4 pilares: click, send_keys, clear, text)
4. Integração completa com o framework BDD

**Tempo**: 7-10 horas | **Ideal para**: Quem nunca programou

---

### 📖 Para Quem Já Programa

**[Docs/](Docs/README.md)** - Documentação completa do framework

Documentos essenciais:
0. **[Docs/00_ESTRUTURA_PROJETO.md](Docs/00_ESTRUTURA_PROJETO.md)** - Visão geral completa 🏗️
1. **[Docs/01_QUICKSTART.md](Docs/01_QUICKSTART.md)** - Início rápido em 5 minutos ⚡
2. **[Docs/02_REFERENCIA_METODOS.md](Docs/02_REFERENCIA_METODOS.md)** - Referência completa de métodos 📖
3. **[Docs/03_BOAS_PRATICAS.md](Docs/03_BOAS_PRATICAS.md)** - Padrões e convenções ✨

Documentos de suporte:
- **[Docs/04_SCREENSHOTS_EXEMPLO.md](Docs/04_SCREENSHOTS_EXEMPLO.md)** - Screenshots 📸
- **[Docs/05_VIDEO_TROUBLESHOOTING.md](Docs/05_VIDEO_TROUBLESHOOTING.md)** - Vídeos 🎥

> 💡 **Dica**: Consulte **[Docs/README.md](Docs/README.md)** para guia completo!

## 🤝 Contribuindo

### Padrões de Código

1. Todo código em português
2. Nomes descritivos e auto-explicativos
3. Docstrings em todos os métodos públicos
4. Sem comentários inline (código deve ser claro)
5. Seguir estrutura numerada (001_, 002_, etc.)

### Commits

Use mensagens claras em português:
- `feat: adiciona cenário de cancelamento de contrato`
- `fix: corrige validação de CPF na tela de quitação`
- `docs: atualiza README com novos exemplos`

## 📄 Licença

[Definir licença do projeto]

## 👥 Equipe

[Informações da equipe]

---

**Dúvidas?** Consulte a documentação ou entre em contato com a equipe de QA.
