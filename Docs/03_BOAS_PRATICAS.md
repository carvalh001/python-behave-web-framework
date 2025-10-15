# ✨ Boas Práticas do Framework

Este documento define as boas práticas e padrões a serem seguidos no framework de automação.

## 🎯 Princípios Fundamentais

### 1. O Código Conta Uma História

✅ **Faça**
```python
def filtrar_contratos_por_situacao_e_pesquisar(self, situacao_contratual):
    """Aplica filtro de situação contratual e executa a pesquisa"""
    self.selecionar_opcao_dropdown(self._CAMPO_DROPDOWN_SITUACAO, situacao_contratual)
    self.clicar_botao_pesquisar()
```

❌ **Evite**
```python
def f(self, s):  # Nome não descritivo
    self.sel(self._dd, s)  # Método abreviado
    self.clk(self._btn)  # Difícil entender
```

### 2. Sem Comentários Inline

O código deve ser auto-explicativo. Use comentários apenas em docstrings.

✅ **Faça**
```python
def calcular_data_vencimento_primeira_parcela(self):
    """Calcula a data de vencimento adicionando 30 dias à data atual"""
    return datetime.now() + timedelta(days=30)
```

❌ **Evite**
```python
def calc_date(self):
    # Pega data atual
    now = datetime.now()
    # Adiciona 30 dias
    future = now + timedelta(days=30)
    # Retorna
    return future
```

### 3. Português em Todo o Código

Exceto palavras técnicas do Selenium/Python que não têm tradução natural.

✅ **Faça**
```python
class PaginaGestaoContratos(PaginaBase):
    _BOTAO_PESQUISAR = (By.ID, "btnPesquisar")
    
    def clicar_botao_pesquisar(self):
        self.clicar_no_elemento(self._BOTAO_PESQUISAR)
```

❌ **Evite**
```python
class ContractManagementPage(BasePage):
    _SEARCH_BUTTON = (By.ID, "btnPesquisar")
    
    def click_search_button(self):
        self.do_click(self._SEARCH_BUTTON)
```

## 📁 Organização de Arquivos

### Estrutura Numerada

Use prefixos numéricos para facilitar navegação e manter ordem lógica:

```
features/
  ├── contrato/
  ├── cliente/
  ├── relatorio/
  └── exemplos/        ⭐ Exemplos ServeRest

pages/
  ├── base_page.py
  ├── contrato/
  │   ├── gestao_contratos_page.py
  │   ├── quitacao_page.py
  │   └── renegociacao_page.py
  ├── cliente/
  │   ├── cadastro_cliente_page.py
  │   └── consulta_cliente_page.py
  └── exemplos/        ⭐ Exemplos didáticos
      ├── login_serverest_page.py
      └── cadastro_serverest_page.py
```

### Nomenclatura de Arquivos

- **Features**: `nome_funcionalidade.feature`
- **Steps**: `modulo_nome_steps.py`
- **Pages**: `nome_page.py`
- **APIs**: `nome_service.py`
- **Utils**: `auxiliar_nome.py` ou `gerenciador_nome.py`

## 🏗️ Padrão Page Object

### Estrutura de uma Page

```python
from selenium.webdriver.common.by import By
from pages.base_page import PaginaBase


class PaginaNome(PaginaBase):
    """
    Descrição clara do que esta página representa.
    Ex: Página de Cadastro de Clientes - permite criar e editar clientes.
    """
    
    # ═══════════════════════════════════════════════════════════
    # LOCALIZADORES
    # ═══════════════════════════════════════════════════════════
    
    _CAMPO_INPUT_NOME = (By.ID, "nome")
    _CAMPO_DROPDOWN_STATUS = (By.ID, "status")
    _BOTAO_SALVAR = (By.XPATH, "//button[text()='Salvar']")
    _TABELA_RESULTADOS = (By.CSS_SELECTOR, "table.results tbody")
    
    # ═══════════════════════════════════════════════════════════
    # INICIALIZAÇÃO
    # ═══════════════════════════════════════════════════════════
    
    def __init__(self, driver, configuracao=None):
        super().__init__(driver)
        self.configuracao = configuracao
        self.url_pagina = self._construir_url()
    
    def _construir_url(self):
        """Constrói a URL da página baseada na configuração"""
        if self.configuracao:
            return f"{self.configuracao.url_base_sistema}/caminho"
        return "https://default.url/caminho"
    
    # ═══════════════════════════════════════════════════════════
    # AÇÕES
    # ═══════════════════════════════════════════════════════════
    
    def carregar_pagina(self):
        """Navega para esta página"""
        self.driver.get(self.url_pagina)
        print(f"[PÁGINA] {self.__class__.__name__} carregada")
    
    def preencher_campo_nome(self, nome):
        """Preenche o campo Nome"""
        self.preencher_campo_texto(self._CAMPO_INPUT_NOME, nome)
        print(f"[FORMULÁRIO] Nome: {nome}")
    
    def clicar_botao_salvar(self):
        """Aciona o botão Salvar"""
        print("[AÇÃO] Salvando")
        self.clicar_no_elemento(self._BOTAO_SALVAR)
    
    # ═══════════════════════════════════════════════════════════
    # VALIDAÇÕES
    # ═══════════════════════════════════════════════════════════
    
    def validar_registro_salvo_com_sucesso(self):
        """Valida que o registro foi salvo"""
        # Implementação
        print("[VALIDAÇÃO] ✓ Registro salvo")
```

### Prefixos de Localizadores

Use prefixos descritivos para identificar o tipo de elemento:

```python
# Botões
_BOTAO_SALVAR
_BOTAO_CANCELAR
_BOTAO_CONFIRMAR

# Campos de Input
_CAMPO_INPUT_NOME
_CAMPO_INPUT_CPF
_CAMPO_INPUT_EMAIL

# Dropdowns/Selects
_CAMPO_DROPDOWN_STATUS
_CAMPO_DROPDOWN_ESTADO

# Tabelas
_TABELA_RESULTADOS
_CORPO_TABELA_CLIENTES

# Labels/Textos
_LABEL_TITULO
_TEXTO_MENSAGEM_SUCESSO

# Links
_LINK_VOLTAR
_LINK_AJUDA

# Modais/Diálogos
_MODAL_CONFIRMACAO
_DIALOGO_ERRO
```

## 📝 Padrão Step Definitions

### Estrutura de Steps

```python
from behave import given, when, then
from project_lib.pages.001_modulo.001_pagina_page import PaginaNome


@given('que condição inicial está satisfeita')
def configurar_condicao_inicial(context):
    """
    Docstring explicando o que este step faz.
    Deve ser claro o suficiente para um júnior entender.
    """
    # Implementação sem comentários inline
    context.pagina = PaginaNome(context.driver, context.configuracao)
    context.pagina.carregar_pagina()


@when('eu executo uma ação')
def executar_acao(context):
    """Executa a ação principal do cenário"""
    context.pagina.executar_acao_principal()


@then('o resultado esperado ocorre')
def validar_resultado(context):
    """Valida que o resultado esperado foi alcançado"""
    context.pagina.validar_resultado_esperado()
```

### Boas Práticas em Steps

✅ **Faça**
```python
@when('eu preencho o formulário com nome "{nome}", CPF "{cpf}" e email "{email}"')
def preencher_formulario(context, nome, cpf, email):
    """Preenche todos os campos do formulário"""
    context.pagina.preencher_campo_nome(nome)
    context.pagina.preencher_campo_cpf(cpf)
    context.pagina.preencher_campo_email(email)
```

❌ **Evite**
```python
@when('eu preencho o formulário')
def preencher_formulario(context):
    # Valores hardcoded - dificulta reutilização
    context.pagina.preencher_campo_nome("João")
    context.pagina.preencher_campo_cpf("123.456.789-00")
```

## 🎭 Padrão BDD - Features

### Estrutura de Feature

```gherkin
# language: pt
Funcionalidade: Nome da Funcionalidade
  Como [papel do usuário]
  Eu quero [ação/funcionalidade]
  Para [benefício/objetivo]

  Contexto: Configuração comum
    Dado que estou autenticado no sistema
    E estou na tela inicial

  @tag1 @tag2
  Cenário: Nome descritivo do cenário
    Dado que existe um registro com ID "123"
    Quando eu acesso a tela de detalhes
    Então os dados do registro são exibidos
    E o status é "Ativo"

  @tag3
  Esquema do Cenário: Nome do cenário com exemplos
    Dado que eu preencho o campo <campo> com "<valor>"
    Quando eu clico em salvar
    Então vejo a mensagem "<mensagem>"

    Exemplos:
      | campo  | valor     | mensagem          |
      | Nome   | João      | Salvo com sucesso |
      | Email  | a@test.com| Salvo com sucesso |
```

### Tags Úteis

```gherkin
@regressivo          # Testes de regressão
@smoke               # Testes básicos/críticos
@video_always        # Sempre gravar vídeo
@wip                 # Work in progress (em desenvolvimento)
@skip                # Pular este teste
@lento               # Teste que demora
```

## 🔧 Configurações (.env)

### Organização do .env

```env
# ═══════════════════════════════════════════════════════════
# URLS DO SISTEMA
# ═══════════════════════════════════════════════════════════
URL_BASE_SISTEMA=https://exemplo.com

# ═══════════════════════════════════════════════════════════
# NAVEGADOR
# ═══════════════════════════════════════════════════════════
NAVEGADOR_TIPO=chrome
NAVEGADOR_HEADLESS=false

# ═══════════════════════════════════════════════════════════
# TIMEOUTS
# ═══════════════════════════════════════════════════════════
TIMEOUT_IMPLICITO=10
```

### Boas Práticas de Configuração

✅ **Faça**
- Use nomes descritivos em MAIÚSCULAS
- Agrupe configurações relacionadas
- Documente com comentários
- Forneça valores padrão razoáveis

❌ **Evite**
- Hardcoded secrets/senhas no código
- Valores mágicos sem explicação
- Configurações misturadas sem organização

## 🎯 Logs e Mensagens

### Padrão de Logs

Use prefixos para categorizar logs:

```python
print("[PÁGINA] Gestão de Contratos carregada")
print("[FILTRO] Aplicando status: Ativo")
print("[AÇÃO] Clicando em Salvar")
print("[FORMULÁRIO] CPF: 123.456.789-00")
print("[VALIDAÇÃO] ✓ Registro salvo com sucesso")
print("[VALIDAÇÃO] ✗ Erro: CPF inválido")
print("[API] POST /contratos")
print("[API-MOCK] Retornando dados mockados")
print("[EVIDÊNCIA] Screenshot capturado")
print("[VÍDEO] Gravação iniciada")
```

### Símbolos Úteis

```python
✓  # Sucesso
✗  # Erro/Falha
→  # Navegação
↓  # Download
↑  # Upload
⚠  # Aviso
ℹ  # Informação
```

## 🧪 Testes e Validações

### Asserções Descritivas

✅ **Faça**
```python
cpf_exibido = self.obter_cpf_da_tela()
assert cpf_exibido == cpf_esperado, \
    f"CPF incorreto. Esperado: '{cpf_esperado}', Encontrado: '{cpf_exibido}'"
```

❌ **Evite**
```python
assert cpf == "123"  # Mensagem genérica do Python
```

### Validações em Múltiplas Etapas

```python
def validar_dados_completos(self, dados_esperados):
    """Valida todos os dados exibidos na tela"""
    erros = []
    
    nome_exibido = self.obter_nome()
    if nome_exibido != dados_esperados['nome']:
        erros.append(f"Nome incorreto: {nome_exibido}")
    
    cpf_exibido = self.obter_cpf()
    if cpf_exibido != dados_esperados['cpf']:
        erros.append(f"CPF incorreto: {cpf_exibido}")
    
    if erros:
        raise AssertionError("\n".join(erros))
    
    print("[VALIDAÇÃO] ✓ Todos os dados estão corretos")
```

## 🚫 Anti-Padrões - O Que Evitar

### 1. Sleep Arbitrário

❌ **Evite**
```python
time.sleep(5)  # Pode ser lento demais ou rápido demais
```

✅ **Faça**
```python
self.clicar_no_elemento(self._BOTAO)  # Espera implícita
```

### 2. Localizadores Frágeis

❌ **Evite**
```python
# XPath absoluto - quebra fácil
(By.XPATH, "/html/body/div[1]/div[2]/table/tr[1]/td[3]")
```

✅ **Faça**
```python
# Seletores relativos e semânticos
(By.ID, "tabelaResultados")
(By.CSS_SELECTOR, "table.resultados td.nome")
```

### 3. Lógica de Negócio nos Steps

❌ **Evite**
```python
@when('eu faço login')
def fazer_login(context):
    # Lógica de UI misturada com step
    context.driver.find_element(By.ID, "user").send_keys("admin")
    context.driver.find_element(By.ID, "pass").send_keys("123")
    context.driver.find_element(By.ID, "btn").click()
```

✅ **Faça**
```python
@when('eu faço login com usuário "{usuario}" e senha "{senha}"')
def fazer_login(context, usuario, senha):
    # Delega para Page Object
    context.pagina_login.realizar_login(usuario, senha)
```

### 4. Código Duplicado

❌ **Evite**
```python
# Mesmo código em vários places
def test_a(context):
    context.driver.get(URL)
    context.driver.maximize_window()
    
def test_b(context):
    context.driver.get(URL)
    context.driver.maximize_window()
```

✅ **Faça**
```python
# Centralizado em Page Object ou helper
def carregar_pagina(self):
    self.driver.get(self.url_pagina)
```

## ✅ Checklist de Qualidade

Antes de fazer commit, verifique:

- [ ] Todos os nomes estão em português e descritivos
- [ ] Não há comentários inline desnecessários
- [ ] Docstrings estão presentes em métodos públicos
- [ ] Logs informativos foram adicionados
- [ ] Não há valores hardcoded (use .env)
- [ ] Código está organizado e segue a estrutura do projeto
- [ ] Testes executam sem erros
- [ ] Linter não aponta problemas

---

**Lembre-se**: Código é lido muito mais vezes do que é escrito. Priorize clareza sobre brevidade!

