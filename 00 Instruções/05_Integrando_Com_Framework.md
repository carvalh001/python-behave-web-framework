# 🔗 Integrando com o Framework

> 💡 **MODO LEITURA**: Tecle **`Ctrl + Shift + V`** para visualização formatada!  
> Muito mais fácil de ler! 

Aprenda como conectar **Features** (Gherkin) → **Steps** (Python) → **Pages** (Selenium) em um fluxo completo!

## 🎭 Os 3 Pilares do Framework BDD

```
1. FEATURE (.feature)     → O QUE testar (linguagem humana)
2. STEP    (.py)          → COMO executar cada passo
3. PAGE    (.py)          → ONDE estão os elementos e ações
```

## 📝 1. Feature - Descrevendo o Teste

### O Que É?

Arquivo `.feature` escrito em **Gherkin** (linguagem próxima do português) que descreve **o comportamento esperado**.

### Estrutura

```gherkin
# language: pt
Funcionalidade: [Nome da funcionalidade]
  Como [papel do usuário]
  Eu quero [ação/funcionalidade]
  Para [benefício/objetivo]

  Cenário: [Nome do cenário]
    Dado que [condição inicial]
    Quando eu [ação do usuário]
    Então [resultado esperado]
```

### Exemplo Real

**Arquivo:** `features/contrato/cadastro_contrato.feature`

```gherkin
# language: pt
Funcionalidade: Cadastro de Contrato
  Como um operador do sistema
  Eu quero cadastrar um novo contrato
  Para registrar operações de crédito

  @cadastro @contrato
  Cenário: Cadastrar contrato com sucesso
    Dado que eu estou na tela de Cadastro de Contratos
    Quando eu preencho o CPF "123.456.789-00"
    E eu preencho o valor "15000,00"
    E eu seleciono a forma de pagamento "Consignado"
    E eu clico no botão Salvar
    Então vejo a mensagem "Contrato cadastrado com sucesso"
    E o número do contrato é exibido
```

**Vantagens:**
- ✅ Qualquer pessoa lê e entende
- ✅ Documenta o comportamento esperado
- ✅ Serve como especificação

## 🔧 2. Step - Implementando os Passos

### O Que É?

Arquivo Python que **implementa** cada linha da Feature.

### Estrutura

```python
from behave import given, when, then

@given('que [condição]')
def nome_funcao(context):
    """Implementação do passo"""
    # código aqui

@when('eu [ação]')
def nome_funcao(context):
    """Implementação do passo"""
    # código aqui

@then('[resultado esperado]')
def nome_funcao(context):
    """Implementação do passo"""
    # código aqui
```

### Exemplo Real

**Arquivo:** `features/steps/contrato_cadastro_steps.py`

```python
from behave import given, when, then
from project_lib.pages.contrato.cadastro_page import PaginaCadastroContrato


@given('que eu estou na tela de Cadastro de Contratos')
def acessar_tela_cadastro(context):
    """Navega para a tela de cadastro"""
    context.pagina_cadastro = PaginaCadastroContrato(
        context.driver,
        context.configuracao
    )
    context.pagina_cadastro.carregar_pagina()


@when('eu preencho o CPF "{cpf}"')
def preencher_cpf(context, cpf):
    """Preenche o campo CPF"""
    context.pagina_cadastro.preencher_campo_cpf(cpf)


@when('eu preencho o valor "{valor}"')
def preencher_valor(context, valor):
    """Preenche o campo valor"""
    context.pagina_cadastro.preencher_campo_valor(valor)


@when('eu seleciono a forma de pagamento "{forma}"')
def selecionar_forma_pagamento(context, forma):
    """Seleciona forma de pagamento"""
    context.pagina_cadastro.selecionar_forma_de_pagamento(forma)


@when('eu clico no botão Salvar')
def clicar_salvar(context):
    """Clica no botão Salvar"""
    context.pagina_cadastro.clicar_botao_salvar()


@then('vejo a mensagem "{mensagem_esperada}"')
def validar_mensagem(context, mensagem_esperada):
    """Valida que a mensagem correta foi exibida"""
    mensagem_na_tela = context.pagina_cadastro.obter_mensagem_sucesso()
    
    assert mensagem_esperada in mensagem_na_tela, \
        f"Mensagem incorreta. Esperado: '{mensagem_esperada}', Encontrado: '{mensagem_na_tela}'"
    
    print(f"[VALIDACAO] [OK] Mensagem: {mensagem_esperada}")


@then('o número do contrato é exibido')
def validar_numero_contrato(context):
    """Valida que número do contrato apareceu"""
    numero = context.pagina_cadastro.obter_numero_contrato()
    
    assert numero, "Número do contrato não foi exibido"
    assert len(numero) > 0, "Número do contrato está vazio"
    
    print(f"[VALIDACAO] [OK] Contrato: {numero}")
```

## 📄 3. Page Object - Representando a Tela

### O Que É?

Classe Python que representa uma **página web** e suas **ações**.

### Estrutura

```python
from selenium.webdriver.common.by import By
from project_lib.pages.base_page import PaginaBase


class PaginaNome(PaginaBase):
    """Descrição da página"""
    
    # LOCALIZADORES
    _CAMPO_X = (By.ID, "x")
    _BOTAO_Y = (By.ID, "y")
    
    def __init__(self, driver, configuracao):
        super().__init__(driver)
        self.configuracao = configuracao
        self.url_pagina = configuracao.url_base + "/caminho"
    
    def carregar_pagina(self):
        """Navega para a página"""
        self.driver.get(self.url_pagina)
    
    def metodo_acao(self):
        """Executa uma ação"""
        self.clicar_no_elemento(self._BOTAO_Y)
```

### Exemplo Real

**Arquivo:** `project_lib/pages/contrato/cadastro_page.py`

```python
from selenium.webdriver.common.by import By
from project_lib.pages.base_page import PaginaBase


class PaginaCadastroContrato(PaginaBase):
    """Página de Cadastro de Contrato"""
    
    # LOCALIZADORES
    _CAMPO_INPUT_CPF = (By.ID, "cpf")
    _CAMPO_INPUT_VALOR = (By.ID, "valorCredito")
    _CAMPO_DROPDOWN_FORMA_PAGAMENTO = (By.ID, "formaPagamento")
    _BOTAO_SALVAR = (By.XPATH, "//button[text()='Salvar']")
    _LABEL_MENSAGEM_SUCESSO = (By.CLASS_NAME, "alert-success")
    _LABEL_NUMERO_CONTRATO = (By.ID, "numeroContrato")
    
    def __init__(self, driver, configuracao):
        super().__init__(driver)
        self.configuracao = configuracao
        self.url_pagina = configuracao.url_base_sistema + "/contrato/novo"
    
    def carregar_pagina(self):
        """Navega para a página de cadastro"""
        self.driver.get(self.url_pagina)
        print(f"[PÁGINA] Cadastro de Contrato carregada")
    
    def preencher_campo_cpf(self, cpf):
        """Preenche o campo CPF"""
        self.preencher_campo_texto(self._CAMPO_INPUT_CPF, cpf)
        print(f"[FORMULÁRIO] CPF: {cpf}")
    
    def preencher_campo_valor(self, valor):
        """Preenche o campo valor do crédito"""
        self.preencher_campo_texto(self._CAMPO_INPUT_VALOR, valor)
        print(f"[FORMULÁRIO] Valor: R$ {valor}")
    
    def selecionar_forma_de_pagamento(self, forma):
        """Seleciona forma de pagamento no dropdown"""
        self.selecionar_opcao_dropdown(self._CAMPO_DROPDOWN_FORMA_PAGAMENTO, forma)
        print(f"[FORMULÁRIO] Forma: {forma}")
    
    def clicar_botao_salvar(self):
        """Clica no botão Salvar"""
        self.clicar_no_elemento(self._BOTAO_SALVAR)
        print("[AÇÃO] Salvando contrato")
    
    def obter_mensagem_sucesso(self):
        """Lê a mensagem de sucesso"""
        mensagem = self.obter_texto_do_elemento(self._LABEL_MENSAGEM_SUCESSO)
        return mensagem
    
    def obter_numero_contrato(self):
        """Lê o número do contrato gerado"""
        numero = self.obter_texto_do_elemento(self._LABEL_NUMERO_CONTRATO)
        return numero
```

## 🔄 O Fluxo Completo

### 1. Usuário Escreve Feature

```gherkin
Quando eu preencho o CPF "123.456.789-00"
```

### 2. Behave Procura Step Correspondente

```python
@when('eu preencho o CPF "{cpf}"')
def preencher_cpf(context, cpf):
    ...
```

### 3. Step Chama Page Object

```python
@when('eu preencho o CPF "{cpf}"')
def preencher_cpf(context, cpf):
    context.pagina_cadastro.preencher_campo_cpf(cpf)
```

### 4. Page Object Usa Selenium

```python
def preencher_campo_cpf(self, cpf):
    self.preencher_campo_texto(self._CAMPO_INPUT_CPF, cpf)
```

### 5. PaginaBase Executa Selenium

```python
def preencher_campo_texto(self, localizador, texto):
    elemento = self._encontrar_elemento(localizador)
    elemento.clear()
    elemento.send_keys(texto)
```

### 6. Selenium Interage com Navegador

```
Python → Selenium → ChromeDriver → Chrome → Página Web
```

## 📊 Diagrama Visual

```
┌─────────────────────────────────────────────────┐
│ FEATURE (Gherkin)                               │
│ "Quando eu preencho o CPF '123.456.789-00'"     │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│ STEP (Python)                                   │
│ context.pagina.preencher_campo_cpf(cpf)         │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│ PAGE OBJECT (Python)                            │
│ self.preencher_campo_texto(_CAMPO_CPF, cpf)     │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│ PAGINA BASE (Python)                            │
│ elemento.clear() + elemento.send_keys(cpf)      │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│ SELENIUM + NAVEGADOR                            │
│ Interage com a página web real                  │
└─────────────────────────────────────────────────┘
```

## 🎯 Exemplo Completo Passo a Passo

Vamos criar um teste completo do zero!

### Passo 1: Criar a Feature

**Arquivo:** `features/contrato/consulta_contrato.feature`

```gherkin
# language: pt
Funcionalidade: Consulta de Contrato
  Como operador
  Eu quero consultar contratos por CPF
  Para verificar informações

  Cenário: Consultar contrato existente
    Dado que eu estou na tela de Consulta
    Quando eu preencho o CPF "123.456.789-00"
    E eu clico em Pesquisar
    Então vejo 1 contrato na lista
    E o status é "Ativo"
```

### Passo 2: Criar o Page Object

**Arquivo:** `project_lib/pages/contrato/consulta_page.py`

```python
from selenium.webdriver.common.by import By
from project_lib.pages.base_page import PaginaBase


class PaginaConsultaContrato(PaginaBase):
    """Página de Consulta de Contratos"""
    
    _CAMPO_CPF = (By.ID, "cpf")
    _BOTAO_PESQUISAR = (By.ID, "btnPesquisar")
    _LINHAS_TABELA = (By.CSS_SELECTOR, "tbody tr")
    _PRIMEIRA_LINHA_STATUS = (By.CSS_SELECTOR, "tbody tr:first-child td.status")
    
    def __init__(self, driver, configuracao):
        super().__init__(driver)
        self.configuracao = configuracao
        self.url_pagina = configuracao.url_base_sistema + "/contrato/consulta"
    
    def carregar_pagina(self):
        """Acessa a página de consulta"""
        self.driver.get(self.url_pagina)
        print("[PÁGINA] Consulta de Contratos carregada")
    
    def preencher_cpf(self, cpf):
        """Preenche o campo CPF"""
        self.preencher_campo_texto(self._CAMPO_CPF, cpf)
        print(f"[FILTRO] CPF: {cpf}")
    
    def clicar_pesquisar(self):
        """Clica no botão Pesquisar"""
        self.clicar_no_elemento(self._BOTAO_PESQUISAR)
        print("[AÇÃO] Pesquisando")
    
    def obter_total_contratos(self):
        """Conta quantos contratos foram encontrados"""
        linhas = self._encontrar_elementos(self._LINHAS_TABELA)
        return len(linhas)
    
    def obter_status_primeiro_contrato(self):
        """Lê o status do primeiro contrato"""
        status = self.obter_texto_do_elemento(self._PRIMEIRA_LINHA_STATUS)
        return status
```

### Passo 3: Criar os Steps

**Arquivo:** `features/steps/contrato_consulta_steps.py`

```python
from behave import given, when, then
from project_lib.pages.contrato.consulta_page import PaginaConsultaContrato


@given('que eu estou na tela de Consulta')
def acessar_tela_consulta(context):
    """Navega para a tela de consulta"""
    context.pagina_consulta = PaginaConsultaContrato(
        context.driver,
        context.configuracao
    )
    context.pagina_consulta.carregar_pagina()


@when('eu preencho o CPF "{cpf}"')
def preencher_cpf(context, cpf):
    """Preenche o filtro de CPF"""
    context.pagina_consulta.preencher_cpf(cpf)


@when('eu clico em Pesquisar')
def clicar_pesquisar(context):
    """Executa a pesquisa"""
    context.pagina_consulta.clicar_pesquisar()


@then('vejo {quantidade:d} contrato na lista')
def validar_quantidade_contratos(context, quantidade):
    """Valida quantidade de contratos encontrados"""
    total = context.pagina_consulta.obter_total_contratos()
    
    assert total == quantidade, \
        f"Quantidade incorreta. Esperado: {quantidade}, Encontrado: {total}"
    
    print(f"[VALIDACAO] [OK] {quantidade} contrato(s)")


@then('o status é "{status_esperado}"')
def validar_status(context, status_esperado):
    """Valida status do contrato"""
    status = context.pagina_consulta.obter_status_primeiro_contrato()
    
    assert status == status_esperado, \
        f"Status incorreto. Esperado: {status_esperado}, Encontrado: {status}"
    
    print(f"[VALIDACAO] [OK] Status: {status_esperado}")
```

### Passo 4: Executar

```bash
behave features/contrato/consulta_contrato.feature
```

## 🎯 Conectando Tudo - Linha por Linha

### Feature Line → Step → Page → Selenium

```gherkin
Dado que eu estou na tela de Consulta
```
↓
```python
@given('que eu estou na tela de Consulta')
def acessar_tela_consulta(context):
    context.pagina_consulta = PaginaConsultaContrato(...)
    context.pagina_consulta.carregar_pagina()
```
↓
```python
def carregar_pagina(self):
    self.driver.get(self.url_pagina)
```
↓
```python
# Selenium abre o navegador na URL
```

---

```gherkin
Quando eu preencho o CPF "123.456.789-00"
```
↓
```python
@when('eu preencho o CPF "{cpf}"')
def preencher_cpf(context, cpf):
    context.pagina_consulta.preencher_cpf(cpf)
```
↓
```python
def preencher_cpf(self, cpf):
    self.preencher_campo_texto(self._CAMPO_CPF, cpf)
```
↓
```python
# PaginaBase
elemento.clear()
elemento.send_keys("123.456.789-00")
```
↓
```python
# Selenium digita no campo
```

## 🔑 Context - Compartilhando Informações

O `context` é um objeto especial que **compartilha dados** entre steps.

### Como Funciona

```python
# No primeiro step
@given('que tenho um CPF')
def definir_cpf(context):
    context.cpf = "123.456.789-00"  # Guarda no context

# No segundo step (pode usar o CPF!)
@when('eu preencho o CPF')
def preencher_cpf(context):
    cpf = context.cpf  # Pega do context
    context.pagina.preencher_cpf(cpf)
```

### No Framework

```python
# Step 1 - Cria página e guarda no context
@given('que estou na tela X')
def acessar_tela(context):
    context.pagina = PaginaX(context.driver, context.configuracao)
    context.pagina.carregar_pagina()

# Step 2 - Usa a página do context
@when('eu clico em algo')
def clicar_algo(context):
    context.pagina.clicar_botao()  # Usa a mesma instância!
```

**Variáveis Comuns no Context:**
- `context.driver` - WebDriver (navegador)
- `context.configuracao` - Configurações do .env
- `context.pagina_X` - Instâncias de Page Objects
- `context.cpf_teste` - Dados compartilhados entre steps

## 📚 Padrões e Boas Práticas

### 1. Um Step = Uma Ação/Validação

✅ **Faça:**
```python
@when('eu preencho o nome "{nome}"')
def preencher_nome(context, nome):
    context.pagina.preencher_campo_nome(nome)

@when('eu preencho o CPF "{cpf}"')
def preencher_cpf(context, cpf):
    context.pagina.preencher_campo_cpf(cpf)
```

❌ **Evite:**
```python
@when('eu preencho tudo')
def preencher_tudo(context):
    # Faz muitas coisas - difícil reutilizar
    context.pagina.preencher_campo_nome("João")
    context.pagina.preencher_campo_cpf("123")
    context.pagina.preencher_campo_email("a@a.com")
```

### 2. Page Object Não Tem Assertions

✅ **Faça:**
```python
# Page Object - apenas retorna o valor
def obter_mensagem(self):
    return self.obter_texto_do_elemento(self._MENSAGEM)

# Step - faz a validação
@then('vejo mensagem "{msg}"')
def validar_mensagem(context, msg):
    mensagem_tela = context.pagina.obter_mensagem()
    assert msg in mensagem_tela  # ← Assertion no STEP
```

❌ **Evite:**
```python
# Page Object com assertion - não faça!
def validar_mensagem(self, msg_esperada):
    msg = self.obter_texto_do_elemento(self._MENSAGEM)
    assert msg == msg_esperada  # ← Não! Assertion no step!
```

### 3. Nomes Descritivos

```python
# ✅ Descritivo
@when('eu preencho o CPF "{cpf}" no filtro de pesquisa')
def preencher_cpf_filtro(context, cpf):
    """Preenche CPF no filtro"""
    context.pagina.preencher_campo_cpf_filtro(cpf)

# ❌ Genérico
@when('eu preencho o campo')
def step_impl(context):
    context.p.fill("123")
```

## 🎯 Exercício Completo

Crie um teste completo para consulta de cliente:

### Feature
```gherkin
# language: pt
Funcionalidade: Consulta de Cliente
  
  Cenário: Buscar cliente por nome
    Dado que eu estou na tela de Consulta de Clientes
    Quando eu preencho o nome "Maria Santos"
    E eu clico em Pesquisar
    Então vejo 1 cliente na lista
    E o CPF é "987.654.321-00"
```

### Page Object
```python
class PaginaConsultaCliente(PaginaBase):
    _CAMPO_NOME = (By.ID, "nome")
    _BOTAO_PESQUISAR = (By.ID, "btnPesquisar")
    _LINHAS = (By.CSS_SELECTOR, "tbody tr")
    _PRIMEIRA_LINHA_CPF = (By.CSS_SELECTOR, "tbody tr:first-child td.cpf")
    
    def preencher_nome(self, nome):
        self.preencher_campo_texto(self._CAMPO_NOME, nome)
    
    def clicar_pesquisar(self):
        self.clicar_no_elemento(self._BOTAO_PESQUISAR)
    
    def obter_total_clientes(self):
        linhas = self._encontrar_elementos(self._LINHAS)
        return len(linhas)
    
    def obter_cpf_primeiro_cliente(self):
        return self.obter_texto_do_elemento(self._PRIMEIRA_LINHA_CPF)
```

### Steps
```python
@given('que eu estou na tela de Consulta de Clientes')
def acessar_consulta(context):
    context.pagina = PaginaConsultaCliente(context.driver, context.configuracao)
    context.pagina.carregar_pagina()

@when('eu preencho o nome "{nome}"')
def preencher_nome(context, nome):
    context.pagina.preencher_nome(nome)

@when('eu clico em Pesquisar')
def clicar_pesquisar(context):
    context.pagina.clicar_pesquisar()

@then('vejo {quantidade:d} cliente na lista')
def validar_quantidade(context, quantidade):
    total = context.pagina.obter_total_clientes()
    assert total == quantidade

@then('o CPF é "{cpf_esperado}"')
def validar_cpf(context, cpf_esperado):
    cpf = context.pagina.obter_cpf_primeiro_cliente()
    assert cpf == cpf_esperado
```

## 💡 Checklist de Criação de Teste

Ao criar um novo teste, siga esta ordem:

- [ ] 1. Escrever Feature em Gherkin (features/modulo/)
- [ ] 2. Identificar localizadores da página (inspecionar HTML)
- [ ] 3. Criar Page Object (project_lib/pages/modulo/)
- [ ] 4. Criar Steps (features/steps/modulo_steps.py)
- [ ] 5. Executar teste
- [ ] 6. Ajustar conforme necessário
- [ ] 7. Validar que funciona
- [ ] 8. Revisar com equipe

## 🎓 Resumo

| Componente | Responsabilidade | Linguagem |
|------------|------------------|-----------|
| **Feature** | Descrever comportamento | Gherkin (português natural) |
| **Step** | Conectar Feature com Page | Python (lógica de teste) |
| **Page** | Interagir com elementos | Python (Selenium) |
| **PaginaBase** | Métodos reutilizáveis | Python (framework) |

## ➡️ Próximo Passo

Parabéns! Você completou os fundamentos. Agora veja o que fazer a seguir:

**[06_Proximos_Passos.md](06_Proximos_Passos.md)** - Exercícios e próxima jornada!

---

**Tempo estimado**: 60 minutos  
**Pré-requisito**: 04_Automacao_Web_Avancado.md  
**Próximo**: Próximos Passos

