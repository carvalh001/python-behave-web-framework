# Framework de Automação de Testes — Portal de Colaboradores

Framework de automação de testes **E2E (end-to-end)** para o **Portal de Colaboradores**, usando **BDD** com Behave e Selenium. Cenários em Gherkin (português), Page Objects e relatórios HTML com evidências (screenshots e vídeos).

---

## Aplicação testada

O **Portal de Colaboradores** é uma aplicação web que permite:

- **Login** com diferentes perfis (Colaborador, Gestor RH, Admin)
- Acesso a funcionalidades conforme o perfil do usuário

O projeto de automação testa o **frontend** do Portal (telas, fluxos e integração com o backend). Para rodar os testes localmente, é necessário ter o **backend** e o **frontend** do Portal em execução (ver [Pré-requisitos](#pré-requisitos) e [Configuração](#2-configuração-do-ambiente)).

---

## Arquitetura do projeto de testes

O framework segue uma arquitetura em camadas, com separação entre cenários (Gherkin), passos (steps) e páginas (Page Objects).

```
python-behave-web-framework/
├── features/                    # Cenários BDD (Gherkin)
│   ├── portal/                 # Testes do Portal de Colaboradores
│   │   └── autenticacao.feature
│   ├── steps/                  # Implementação dos passos (Dado/Quando/Então)
│   │   ├── portal_auth_steps.py
│   │   └── steps_comuns_login.py
│   └── environment.py          # Hooks (antes/depois dos cenários, navegador, evidências)
│
├── pages/                      # Page Objects (uma classe por tela)
│   ├── base_page.py            # Classe base (Selenium, waits, helpers)
│   └── portal/
│       └── login_portal_page.py # Página de login do Portal
│
├── recursos/                   # Infraestrutura compartilhada
│   ├── utils/                  # Gerenciadores (configuração, navegador, evidências, relatório)
│   └── apis/                   # Serviços de API (quando necessário)
│
├── reports/                    # Relatórios e evidências (gerados na execução)
├── generate_report.py          # Gera relatório HTML a partir do JSON do Behave
├── behave.ini                  # Configuração do Behave (formatos, idioma)
├── requirements.txt            # Dependências Python
└── .env                        # Variáveis de ambiente (URLs, navegador, timeouts) — não versionado
```

**Fluxo de execução:**

1. **Behave** lê os arquivos `.feature` e chama os **steps** correspondentes.
2. Os **steps** usam os **Page Objects** para interagir com a aplicação (clicar, preencher, validar).
3. O **environment.py** inicia o navegador, aplica configurações do `.env` e registra evidências (screenshots/vídeos).
4. Ao final, o **generate_report.py** pode ser usado para gerar o relatório HTML a partir de `reports/results.json`.

---

## Pré-requisitos

- **Python 3.11+** (recomendado 3.11 ou 3.12)
- **pip** (geralmente já vem com o Python)
- **Google Chrome** ou **Chromium** (para os testes E2E; o ChromeDriver é gerenciado automaticamente pelo `webdriver-manager`)
- **Portal de Colaboradores** (para testes contra o sistema real):
  - **Backend** rodando (ex.: API do portal) com dados de teste (seed com usuários)
  - **Frontend** rodando (ex.: `npm run dev` em `http://localhost:5173`)

Em **Linux**, se o Chrome não estiver instalado:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y chromium-browser

# Fedora
sudo dnf install chromium
```

---

## Setup

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd python-behave-web-framework
```

### 2. Criar ambiente virtual

O uso de ambiente virtual é recomendado para isolar as dependências do projeto.

**Windows (PowerShell ou CMD):**

```powershell
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
.\venv\Scripts\activate
```

**Windows (Git Bash):**

```bash
python -m venv venv
source venv/Scripts/activate
```

**Linux e macOS:**

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate
```

Após ativar, o prompt deve exibir `(venv)` no início.

### 3. Instalar dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie o arquivo de exemplo e ajuste conforme o ambiente (URL do Portal, navegador, etc.):

```bash
# Windows (PowerShell/CMD)
copy .env.exemplo .env

# Linux/macOS
cp .env.exemplo .env
```

Edite o `.env` e defina pelo menos a URL do frontend do Portal:

```env
# URL do frontend do Portal de Colaboradores (ex.: local ou Railway)
URL_BASE_SISTEMA=http://localhost:5173

# Navegador (chrome, firefox, edge)
NAVEGADOR_TIPO=chrome
NAVEGADOR_HEADLESS=false
```

Outras variáveis (timeouts, diretórios de relatório, screenshots, vídeos) estão documentadas no próprio `.env.exemplo`.

---

## Executando os testes

Com o ambiente virtual ativado e o `.env` configurado:

### Executar todos os cenários do Portal

```bash
behave features/portal/
```

### Executar apenas a feature de autenticação

```bash
behave features/portal/autenticacao.feature
```

### Executar por tag

```bash
# Todos os cenários marcados com @portal
behave features/portal/ --tags=@portal

# Apenas cenários de login
behave features/portal/ --tags=@login
```

### Saída no console e JSON

Por padrão, o Behave usa o `behave.ini` e gera:

- Saída **pretty** no console
- Arquivo **`reports/results.json`** para relatórios

Para gerar também **JUnit XML** (útil para CI):

```bash
behave features/portal/autenticacao.feature --tags=@portal --junit --junit-directory reports
```

### Gerar relatório HTML

Após rodar os testes, gere o relatório HTML a partir do JSON:

```bash
python generate_report.py
```

O relatório é criado em `reports/AAAA/Mês/Testes - AAAA-MM-DD HHhMM/` e pode abrir no navegador automaticamente, conforme `RELATORIO_ABRIR_AUTOMATICAMENTE` no `.env`.

---

## Perfis de teste (autenticação)

Os cenários de login usam credenciais compatíveis com o seed do backend:

| Perfil        | Usuário | Senha    |
|---------------|---------|----------|
| Colaborador   | maria   | 123456   |
| Gestor RH     | joao    | 123456   |
| Admin         | admin   | admin123 |

---

## Relatórios e evidências

- **Relatório HTML:** executar `python generate_report.py` após os testes; saída em `reports/AAAA/Mês/Testes - .../`.
- **Screenshots:** em falhas (e opcionalmente em todos os passos), em `reports/screenshots/` (ou na pasta do relatório gerado).
- **Vídeos:** opcional, configurável via `.env` (`GRAVAR_VIDEO_SEMPRE`, etc.).

---

## CI/CD (GitHub Actions)

O projeto inclui um workflow em `.github/workflows/testar-portal.yml` que:

- Dispara em **push na branch `main`**, em **schedule** (diário) e em **workflow_dispatch**.
- Instala Python e Chrome, executa os testes do Portal, publica resultados JUnit no GitHub (check run e Job Summary com tabela de cenários) e faz upload do relatório como artefato.

Não é necessário configurar nada extra no repositório além das permissões já definidas no workflow.

---

## Documentação adicional

- **[Docs/10_TESTES_PORTAL.md](Docs/10_TESTES_PORTAL.md)** — Detalhes dos testes do Portal (pré-requisitos, comandos, perfis).
- **[Docs/01_QUICKSTART.md](Docs/01_QUICKSTART.md)** — Início rápido do framework (se existir).
- **[.env.exemplo](.env.exemplo)** — Referência de todas as variáveis de ambiente.

---

## Resumo rápido (Linux)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.exemplo .env
# Editar .env com URL_BASE_SISTEMA (ex.: http://localhost:5173)
behave features/portal/autenticacao.feature --tags=@portal
python generate_report.py
```

## Resumo rápido (Windows)

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.exemplo .env
# Editar .env com URL_BASE_SISTEMA (ex.: http://localhost:5173)
behave features/portal/autenticacao.feature --tags=@portal
python generate_report.py
```
