# 📚 Referência Rápida de Métodos

Guia de referência dos métodos disponíveis no framework.

## 🎯 PaginaBase - Métodos Principais

Todos os Page Objects herdam de `PaginaBase`, que fornece métodos reutilizáveis.

### 🖱️ Métodos de Interação

#### `clicar_no_elemento(localizador)`
Clica em um elemento após garantir que ele está clicável.

```python
self.clicar_no_elemento(self._BOTAO_SALVAR)
```

#### `preencher_campo_texto(localizador, texto)`
Limpa e preenche um campo de texto.

```python
self.preencher_campo_texto(self._CAMPO_CPF, "123.456.789-00")
```

#### `selecionar_opcao_dropdown(localizador, texto_visivel)`
Seleciona uma opção em um dropdown (select) pelo texto.

```python
self.selecionar_opcao_dropdown(self._DROPDOWN_STATUS, "Ativo")
```

### 📖 Métodos de Leitura

#### `obter_texto_do_elemento(localizador, aguardar_texto_aparecer=False, timeout=10)`
Obtém o texto de um elemento.

```python
texto = self.obter_texto_do_elemento(self._LABEL_NOME)
```

#### `obter_texto_com_retentativa(localizador, padrao_esperado=None, tentativas_maximas=3, espera_entre_tentativas=1)`
Obtém texto com múltiplas tentativas (útil para conteúdo dinâmico).

```python
cpf = self.obter_texto_com_retentativa(
    self._CAMPO_CPF,
    padrao_esperado="123",
    tentativas_maximas=5
)
```

#### `obter_titulo_pagina()`
Retorna o título da página (tag `<title>`).

```python
titulo = self.obter_titulo_pagina()
```

### ✅ Métodos de Validação

#### `elemento_esta_visivel(localizador)`
Verifica se um elemento está visível (retorna True/False).

```python
if self.elemento_esta_visivel(self._BOTAO_SALVAR):
    print("Botão está visível")
```

### 🔍 Métodos Internos (Protegidos)

#### `_encontrar_elemento(localizador)`
Encontra um único elemento com espera explícita.

```python
elemento = self._encontrar_elemento(self._BOTAO_OK)
```

#### `_encontrar_elementos(localizador)`
Encontra múltiplos elementos com espera explícita.

```python
linhas = self._encontrar_elementos(self._LINHAS_TABELA)
for linha in linhas:
    print(linha.text)
```

## 📍 Criando Localizadores

Localizadores são tuplas que identificam elementos na página.

### Exemplos de Localizadores

```python
from selenium.webdriver.common.by import By

# Por ID
_BOTAO_SALVAR = (By.ID, "btnSalvar")

# Por XPATH
_CAMPO_NOME = (By.XPATH, "//input[@name='nome']")

# Por CSS Selector
_TABELA_RESULTADOS = (By.CSS_SELECTOR, "table.resultados tbody")

# Por Class Name
_MENSAGEM_ERRO = (By.CLASS_NAME, "error-message")

# Por Name
_CAMPO_EMAIL = (By.NAME, "email")

# Por Link Text
_LINK_VOLTAR = (By.LINK_TEXT, "Voltar")

# Por Partial Link Text
_LINK_AJUDA = (By.PARTIAL_LINK_TEXT, "Ajuda")

# Por Tag Name
_TODAS_IMAGENS = (By.TAG_NAME, "img")
```

### Localizadores Dinâmicos

Para elementos que variam baseado em dados:

```python
def abrir_menu_por_cpf(self, cpf):
    """Abre menu de um CPF específico"""
    localizador_dinamico = (
        By.XPATH,
        f"//tr[contains(., '{cpf}')]//button[@class='menu']"
    )
    self.clicar_no_elemento(localizador_dinamico)
```

## 🛠️ Métodos da Classe AuxiliarDatas

### `obter_dia_posterior()`
Retorna a data de amanhã.

```python
from recursos.utils.auxiliar_datas import AuxiliarDatas

data = AuxiliarDatas.obter_dia_posterior()
# Retorna: "16/10/2025"
```

### `obter_data_um_mes_e_dois_dias()`
Retorna data com 1 mês e 2 dias no futuro.

```python
data = AuxiliarDatas.obter_data_um_mes_e_dois_dias()
# Retorna: "16/11/2025"
```

### `obter_data_com_deslocamento(quantidade_dias, quantidade_meses)`
Calcula data com deslocamento personalizado.

```python
# 15 dias no futuro
data = AuxiliarDatas.obter_data_com_deslocamento(quantidade_dias=15)

# 2 meses atrás
data = AuxiliarDatas.obter_data_com_deslocamento(quantidade_meses=-2)

# 1 mês e 5 dias no futuro
data = AuxiliarDatas.obter_data_com_deslocamento(
    quantidade_dias=5,
    quantidade_meses=1
)
```

### `obter_data_atual()`
Retorna a data de hoje.

```python
data = AuxiliarDatas.obter_data_atual()
# Retorna: "15/10/2025"
```

### `obter_data_atual_com_horario()`
Retorna data e hora atuais.

```python
data_hora = AuxiliarDatas.obter_data_atual_com_horario()
# Retorna: "15/10/2025 14:30:45"
```

### `converter_data_para_formato_api(data_brasileira)`
Converte data de DD/MM/YYYY para YYYY-MM-DD.

```python
data_api = AuxiliarDatas.converter_data_para_formato_api("15/10/2025")
# Retorna: "2025-10-15"
```

## 🌐 ServicoContrato - API

### `criar_contrato(**campos_personalizados)`
Cria um contrato via API (ou mock).

```python
from recursos.apis.contrato_service import ServicoContrato

servico = ServicoContrato(configuracao=context.configuracao)

# Criar com valores padrão
resposta = servico.criar_contrato()

# Criar com situação específica
resposta = servico.criar_contrato(situacaoContrato=2)

# Criar com múltiplos campos personalizados
resposta = servico.criar_contrato(
    situacaoContrato=1,
    prazo=36,
    valorCredito=50000
)
```

## 📋 Padrões de Nomenclatura

### Variáveis de Localizador

Use MAIÚSCULAS com prefixo descritivo:

```python
_BOTAO_CONFIRMAR
_CAMPO_INPUT_CPF
_CAMPO_DROPDOWN_STATUS
_TABELA_RESULTADOS
_LINK_VOLTAR
_LABEL_MENSAGEM_SUCESSO
```

### Métodos de Ação

Use verbos no infinitivo:

```python
def clicar_botao_salvar(self):
    """Clica no botão Salvar"""
    pass

def preencher_formulario_completo(self, dados):
    """Preenche todos os campos do formulário"""
    pass

def selecionar_primeira_opcao(self):
    """Seleciona a primeira opção da lista"""
    pass
```

### Métodos de Validação

Use verbos que indicam verificação:

```python
def validar_mensagem_sucesso(self):
    """Valida se mensagem de sucesso foi exibida"""
    pass

def verificar_tabela_vazia(self):
    """Verifica se a tabela não tem resultados"""
    pass

def confirmar_dados_exibidos(self, dados_esperados):
    """Confirma que os dados corretos estão na tela"""
    pass
```

### Métodos de Obtenção

Use prefixo `obter_`:

```python
def obter_total_registros(self):
    """Obtém o total de registros da tabela"""
    pass

def obter_mensagem_erro(self):
    """Obtém o texto da mensagem de erro"""
    pass
```

## 💡 Dicas de Uso

### Esperas Inteligentes

```python
# ❌ Evite sleep fixo
time.sleep(5)

# ✅ Use esperas explícitas
self.clicar_no_elemento(self._BOTAO)  # Já espera elemento estar clicável

# ✅ Para textos dinâmicos, use retry
texto = self.obter_texto_com_retentativa(
    self._CAMPO_VALOR,
    tentativas_maximas=5
)
```

### Reutilização de Código

```python
# ✅ Crie métodos compostos
def preencher_formulario_cliente(self, nome, cpf, email):
    """Preenche formulário completo do cliente"""
    self.preencher_campo_texto(self._CAMPO_NOME, nome)
    self.preencher_campo_texto(self._CAMPO_CPF, cpf)
    self.preencher_campo_texto(self._CAMPO_EMAIL, email)
    self.clicar_botao_salvar()
```

### Logs Descritivos

```python
# ✅ Adicione prints informativos
def filtrar_por_status(self, status):
    """Filtra resultados por status"""
    print(f"[FILTRO] Aplicando filtro de status: {status}")
    self.selecionar_opcao_dropdown(self._DROPDOWN_STATUS, status)
    self.clicar_botao_filtrar()
    print("[FILTRO] ✓ Filtro aplicado")
```

## 🎯 Exemplos Completos

### Page Object Completo

```python
from selenium.webdriver.common.by import By
from pages.base_page import PaginaBase


class PaginaCadastroCliente(PaginaBase):
    """Página de Cadastro de Cliente"""
    
    _CAMPO_INPUT_NOME = (By.ID, "nome")
    _CAMPO_INPUT_CPF = (By.ID, "cpf")
    _CAMPO_INPUT_EMAIL = (By.ID, "email")
    _CAMPO_DROPDOWN_ESTADO = (By.ID, "estado")
    _BOTAO_SALVAR = (By.XPATH, "//button[text()='Salvar']")
    _MENSAGEM_SUCESSO = (By.CLASS_NAME, "alert-success")
    
    def __init__(self, driver, configuracao=None):
        super().__init__(driver)
        self.configuracao = configuracao
        self.url_pagina = configuracao.url_base_sistema + "/cadastro" if configuracao else None
    
    def carregar_pagina(self):
        """Navega para a página de cadastro"""
        if self.url_pagina:
            self.driver.get(self.url_pagina)
            print(f"[PÁGINA] Cadastro carregada: {self.url_pagina}")
    
    def preencher_dados_cliente(self, nome, cpf, email, estado):
        """Preenche todos os dados do cliente"""
        print(f"[FORMULÁRIO] Preenchendo dados do cliente: {nome}")
        self.preencher_campo_texto(self._CAMPO_INPUT_NOME, nome)
        self.preencher_campo_texto(self._CAMPO_INPUT_CPF, cpf)
        self.preencher_campo_texto(self._CAMPO_INPUT_EMAIL, email)
        self.selecionar_opcao_dropdown(self._CAMPO_DROPDOWN_ESTADO, estado)
    
    def clicar_botao_salvar(self):
        """Aciona o botão Salvar"""
        print("[AÇÃO] Salvando cadastro")
        self.clicar_no_elemento(self._BOTAO_SALVAR)
    
    def validar_cadastro_realizado_com_sucesso(self):
        """Valida que mensagem de sucesso foi exibida"""
        mensagem_visivel = self.elemento_esta_visivel(self._MENSAGEM_SUCESSO)
        assert mensagem_visivel, "Mensagem de sucesso não foi exibida"
        print("[VALIDAÇÃO] ✓ Cadastro realizado com sucesso")
```

### Step Definition Completo

```python
from behave import given, when, then
from pages.cliente.cadastro_cliente_page import PaginaCadastroCliente


@given('que eu estou na página de cadastro de cliente')
def acessar_pagina_cadastro(context):
    """Navega para a página de cadastro"""
    context.pagina_cadastro = PaginaCadastroCliente(
        context.driver,
        context.configuracao
    )
    context.pagina_cadastro.carregar_pagina()


@when('eu preencho os dados do cliente com nome "{nome}", CPF "{cpf}", email "{email}" e estado "{estado}"')
def preencher_dados_cliente(context, nome, cpf, email, estado):
    """Preenche formulário de cadastro"""
    context.pagina_cadastro.preencher_dados_cliente(nome, cpf, email, estado)


@when('eu clico no botão Salvar')
def clicar_salvar(context):
    """Salva o cadastro"""
    context.pagina_cadastro.clicar_botao_salvar()


@then('o cadastro é realizado com sucesso')
def validar_cadastro_sucesso(context):
    """Valida sucesso do cadastro"""
    context.pagina_cadastro.validar_cadastro_realizado_com_sucesso()
```

---

**Dúvidas?** Consulte os exemplos em `project_lib/pages/001_contrato/` ou o README principal.

