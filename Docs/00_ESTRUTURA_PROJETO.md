# 🏗️ Estrutura do Projeto

Documento visual da organização completa do Framework de Automação.

## 📁 Visão Geral da Raiz

```
Siepex/
├── README.md                    ⭐ COMECE AQUI - Documentação principal
├── .env                         🔧 Configurações
├── .env.exemplo                 📋 Template de configuração
├── behave.ini                   ⚙️ Configurações do Behave
├── requirements.txt             📦 Dependências Python
├── generate_report.py           📊 Gerador de relatórios HTML
│
├── 00 Instruções/               🎓 TUTORIAIS PYTHON DO ZERO
│   ├── README.md                    📖 Índice dos tutoriais
│   ├── 01_Python_Variaveis_Listas.md
│   ├── 02_Python_Metodos_Classes.md
│   ├── 03_Automacao_Web_Basico.md
│   ├── 04_Automacao_Web_Avancado.md
│   ├── 05_Integrando_Com_Framework.md
│   └── 06_Proximos_Passos.md
│
├── Docs/                        📚 DOCUMENTAÇÃO DO FRAMEWORK
│   ├── README.md                    📖 Guia da documentação
│   ├── 00_ESTRUTURA_PROJETO.md      🏗️ Este arquivo
│   ├── 01_QUICKSTART.md             ⚡ Início rápido
│   ├── 02_REFERENCIA_METODOS.md     📚 Referência completa
│   ├── 03_BOAS_PRATICAS.md          ✨ Padrões
│   ├── 04_SCREENSHOTS_EXEMPLO.md    📸 Screenshots
│   └── 05_VIDEO_TROUBLESHOOTING.md  🎥 Vídeos
│
├── features/                    🎭 TESTES BDD (Analistas trabalham aqui)
│   ├── contrato/                    (Testes do sistema)
│   │   ├── quitacao_contrato.feature
│   │   └── renegociacao_contrato.feature
│   ├── exemplos/                    ⭐ (Exemplos ServeRest)
│   │   ├── login_serverest.feature
│   │   └── cadastro_serverest.feature
│   ├── steps/
│   │   ├── contrato_quitacao_steps.py
│   │   ├── contrato_renegociacao_steps.py
│   │   └── exemplos_serverest_steps.py ⭐
│   └── environment.py               🎯 Hooks do Behave (90 linhas)
│
├── pages/                       📄 PAGE OBJECTS (Mesmo nível!)
│   ├── base_page.py                 🏛️ Classe base (PaginaBase)
│   ├── contrato/                    (Pages do sistema)
│   │   ├── gestao_contratos_page.py
│   │   ├── quitacao_page.py
│   │   └── renegociacao_page.py
│   └── exemplos/                    ⭐ (Pages ServeRest)
│       ├── login_serverest_page.py
│       └── cadastro_serverest_page.py
│
├── recursos/                    🔧 INFRAESTRUTURA (antes project_lib)
│   ├── apis/                        🌐 Serviços de API (antes services)
│   │   └── contrato_service.py
│   └── utils/                       🛠️ Utilitários
│       ├── auxiliar_datas.py
│       ├── gerenciador_configuracao.py
│       ├── gerenciador_navegador.py
│       ├── gerenciador_evidencias.py
│       ├── gerenciador_relatorio.py
│       ├── gravador_video.py
│       └── video_converter.py
│
├── reports/                     📊 Relatórios gerados
│   └── 2025/Outubro/...
│
└── venv/                        🐍 Ambiente virtual Python
```

## 🎯 Onde os Analistas Trabalham

### ✅ MEXE AQUI (Criação de Testes)

```
features/contrato/     ← 1. Escrever cenários (.feature)
features/steps/        ← 2. Implementar passos (steps)
pages/contrato/        ← 3. Criar Page Objects
```

**📚 Para Aprender:**
```
features/exemplos/     ← Exemplos ServeRest (executáveis!)
pages/exemplos/        ← Page Objects de exemplo
```

### ⚠️ NÃO MEXE (Infraestrutura)

```
recursos/utils/              ← Gerenciadores (apenas consultar)
recursos/apis/               ← Serviços de API
features/environment.py      ← Hooks do Behave (já configurado)
behave.ini                   ← Configuração do framework
generate_report.py           ← Gerador de relatórios
```

## 📚 Ordem de Leitura da Documentação

Para analistas iniciando no framework:

```
1. 📖 README.md (na raiz)
   ↓
2. ⚡ Docs/01_QUICKSTART.md
   ↓
3. 📚 Docs/02_REFERENCIA_METODOS.md
   ↓
4. ✨ Docs/03_BOAS_PRATICAS.md
   ↓
5. Começar a criar testes! 🚀
```

Documentos de suporte (consultar quando necessário):
- 📸 04_SCREENSHOTS_EXEMPLO.md
- 🎥 05_VIDEO_TROUBLESHOOTING.md

## 🔄 Fluxo de Trabalho

### Criar um Novo Teste

```mermaid
1. Escrever cenário     → features/contrato/*.feature
2. Implementar steps    → features/steps/contrato_*_steps.py
3. Criar Page Object    → project_lib/pages/contrato/*_page.py
4. Executar teste       → behave
5. Ver relatório        → reports/.../*.html
```

### Estrutura de um Módulo Completo

```
Exemplo: Módulo "Cliente"

features/cliente/
  └── cadastro_cliente.feature       ← Cenários Gherkin

features/steps/
  └── cliente_cadastro_steps.py      ← Implementação dos passos

project_lib/pages/cliente/
  └── cadastro_cliente_page.py       ← Page Object
```

## 📋 Arquivos de Configuração

### .env (Essencial!)
```env
URL_BASE_SISTEMA=https://...
NAVEGADOR_TIPO=chrome
TIMEOUT_IMPLICITO=10
API_MODO_MOCK=true
...
```

### behave.ini
```ini
[behave]
paths = ./features
format = pretty, json.pretty
lang = pt
```

### requirements.txt
```txt
behave
selenium
webdriver-manager
python-dotenv
requests
...
```

## 🎨 Convenções de Nomenclatura

### Arquivos Features
```
features/modulo/nome_funcionalidade.feature
Exemplo: quitacao_contrato.feature
```

### Arquivos Steps
```
features/steps/modulo_funcionalidade_steps.py
Exemplo: contrato_quitacao_steps.py
```

### Arquivos Pages
```
project_lib/pages/modulo/nome_page.py
Exemplo: gestao_contratos_page.py
```

### Classes
```python
# Pages
class PaginaNomeDaTela(PaginaBase):
    ...

# Services
class ServicoNome:
    ...

# Helpers
class AuxiliarNome:
    ...
```

## 🚀 Comandos Principais

```bash
# Ativar ambiente virtual
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar todos os testes
behave

# Executar teste específico
behave --tags=@quitacao

# Gerar relatório
python generate_report.py
```

## 📊 Relatórios

Os relatórios são automaticamente organizados por data:

```
reports/
└── 2025/
    └── Outubro/
        └── Testes - 2025-10-15 16h33/
            ├── report_15-10-2025_16-33.html      📄 Abrir no browser
            ├── results_15-10-2025_16-33.json
            ├── screenshots_15-10-2025_16-33/     📸
            └── videos_15-10-2025_16-33/          🎥
```

## 💡 Dicas Importantes

### ✅ Boas Práticas

1. **Sempre** crie o arquivo `.env` antes de rodar testes
2. **Sempre** leia as boas práticas antes de criar código
3. **Sempre** use nomes descritivos em português
4. **Sempre** adicione docstrings nos métodos

### ⚠️ Atenção

1. **Não** use números no início de nomes de diretórios Python
2. **Não** use caracteres Unicode (✓, ✗) em prints
3. **Não** faça hardcode de URLs (use .env)
4. **Não** ignore as convenções de nomenclatura

## 🆘 Precisa de Ajuda?

1. **Dúvida sobre estrutura?** → Este arquivo
2. **Como começar?** → Docs/01_QUICKSTART.md
3. **Qual método usar?** → Docs/02_REFERENCIA_METODOS.md
4. **Está fazendo certo?** → Docs/03_BOAS_PRATICAS.md
5. **Erro de execução?** → Docs/05_VIDEO_TROUBLESHOOTING.md ou Docs/08_CORRECOES_FINAIS.md

---

**Última atualização**: 15/10/2025  
**Versão do Framework**: 2.0 - Júnior Friendly

