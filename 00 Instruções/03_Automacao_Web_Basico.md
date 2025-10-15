# 🌐 Automação Web - Conceitos Básicos

> 💡 **VISUALIZAÇÃO**: Aperte **`Ctrl + Shift + V`** para ver formatado!  
> Muito mais fácil de ler! 

Aprenda os fundamentos da automação web com Selenium. **Automação web é simples: você só faz 4 coisas!**

## 🎯 Os 4 Pilares da Automação Web

```
1. CLICAR       (click)      → Acionar botões, links, etc
2. PREENCHER    (send_keys)  → Digitar em campos
3. LIMPAR       (clear)      → Apagar conteúdo de campos
4. LER          (text)       → Obter textos da tela
```

**É só isso!** Todo teste de automação web é uma combinação dessas 4 ações.

---

## 🌐 Site de Prática: ServeRest

Vamos usar o **[ServeRest](https://front.serverest.dev)** - um site público e gratuito para praticar automação!

**URLs para praticar:**
- Login: https://front.serverest.dev/login
- Cadastro: https://front.serverest.dev/cadastrarusuarios

**Vantagens:**
- ✅ Grátis e sempre disponível
- ✅ Não precisa credenciais
- ✅ Interface simples e clara
- ✅ Perfeito para aprender

**Você pode executar TODOS os exemplos deste tutorial no ServeRest!**

## 🖱️ 1. CLICAR (click)

### Conceito
Simula o clique do mouse em um elemento.

### Código Puro (Selenium)
```python
from selenium.webdriver.common.by import By

# Encontrar elemento
botao = driver.find_element(By.ID, "btnSalvar")

# Clicar
botao.click()
```

### No Framework (PaginaBase)
```python
# Definimos o localizador
_BOTAO_SALVAR = (By.ID, "btnSalvar")

# Usamos o método do framework
self.clicar_no_elemento(self._BOTAO_SALVAR)
```

### Exemplos Práticos

```python
# Clicar em botão
self.clicar_no_elemento(self._BOTAO_PESQUISAR)

# Clicar em link
self.clicar_no_elemento(self._LINK_VOLTAR)

# Clicar em checkbox
self.clicar_no_elemento(self._CHECKBOX_ACEITO)

# Clicar em item de menu
self.clicar_no_elemento(self._MENU_QUITACAO)
```

**No Step:**
```python
@when('eu clico no botão Salvar')
def clicar_salvar(context):
    """Clica no botão Salvar"""
    context.pagina.clicar_botao_salvar()
```

## ⌨️ 2. PREENCHER (send_keys)

### Conceito
Simula digitação do teclado em um campo de texto.

### Código Puro (Selenium)
```python
# Encontrar campo
campo_nome = driver.find_element(By.ID, "nome")

# Limpar campo (boa prática)
campo_nome.clear()

# Preencher
campo_nome.send_keys("João Silva")
```

### No Framework (PaginaBase)
```python
# Definimos o localizador
_CAMPO_NOME = (By.ID, "nome")

# Usamos o método do framework (já limpa e preenche)
self.preencher_campo_texto(self._CAMPO_NOME, "João Silva")
```

### Exemplos Práticos

```python
# Preencher texto
self.preencher_campo_texto(self._CAMPO_NOME, "João Silva")

# Preencher CPF
self.preencher_campo_texto(self._CAMPO_CPF, "123.456.789-00")

# Preencher data
self.preencher_campo_texto(self._CAMPO_DATA, "15/10/2025")

# Preencher valor
self.preencher_campo_texto(self._CAMPO_VALOR, "1500,00")
```

**No Step:**
```python
@when('eu preencho o nome "{nome}"')
def preencher_nome(context, nome):
    """Preenche o campo nome"""
    context.pagina.preencher_campo_nome(nome)
```

## 🧹 3. LIMPAR (clear)

### Conceito
Remove todo o conteúdo de um campo de texto.

### Código Puro (Selenium)
```python
# Encontrar campo
campo = driver.find_element(By.ID, "desconto")

# Limpar
campo.clear()
```

### No Framework
```python
# Geralmente já incluído no preencher_campo_texto
# Mas se precisar limpar sem preencher:

elemento = self._encontrar_elemento(self._CAMPO_DESCONTO)
elemento.clear()
```

### Exemplo Prático do Framework

```python
def limpar_campo_desconto(self):
    """Limpa o campo desconto"""
    elemento = self._encontrar_elemento(self._CAMPO_DESCONTO)
    elemento.clear()
    
    # Extra: garantir limpeza total
    from selenium.webdriver.common.keys import Keys
    for _ in range(3):
        elemento.send_keys(Keys.BACKSPACE)
    
    print("[FORMULÁRIO] Campo Desconto limpo")
```

**No Step:**
```python
@when('eu limpo o campo "{nome_campo}"')
def limpar_campo(context, nome_campo):
    """Limpa um campo específico"""
    context.pagina.limpar_campo_por_nome(nome_campo)
```

## 📖 4. LER (text / get_attribute)

### Conceito
Obtém informações exibidas na tela ou atributos de elementos.

### Código Puro (Selenium)
```python
# Ler texto visível
elemento = driver.find_element(By.ID, "cpfCliente")
texto = elemento.text
print(f"CPF: {texto}")  # CPF: 123.456.789-00

# Ler atributo
campo = driver.find_element(By.ID, "inputNome")
valor = campo.get_attribute("value")
print(f"Valor: {valor}")
```

### No Framework (PaginaBase)
```python
# Ler texto de elemento
cpf = self.obter_texto_do_elemento(self._CAMPO_CPF)

# Com retry para conteúdo dinâmico
cpf = self.obter_texto_com_retentativa(
    self._CAMPO_CPF,
    tentativas_maximas=3
)
```

### Exemplos Práticos

```python
# Ler CPF da tela
def obter_cpf_exibido(self):
    """Obtém CPF mostrado na tela"""
    cpf = self.obter_texto_do_elemento(self._CAMPO_CPF)
    return cpf

# Ler mensagem de sucesso
def obter_mensagem_sucesso(self):
    """Obtém texto da mensagem"""
    mensagem = self.obter_texto_do_elemento(self._LABEL_MENSAGEM)
    return mensagem

# Ler valor de tabela
def obter_primeira_prestacao(self):
    """Obtém valor da primeira prestação"""
    valor = self.obter_texto_do_elemento(self._PRIMEIRA_PRESTACAO)
    return valor
```

**No Step (validação):**
```python
@then('o CPF "{cpf_esperado}" é exibido')
def validar_cpf(context, cpf_esperado):
    """Valida que o CPF correto está na tela"""
    cpf_na_tela = context.pagina.obter_cpf_exibido()
    
    assert cpf_na_tela == cpf_esperado, \
        f"CPF incorreto. Esperado: {cpf_esperado}, Encontrado: {cpf_na_tela}"
    
    print("[VALIDAÇÃO] [OK] CPF correto")
```

## 🎯 Localizadores - Como Encontrar Elementos

Para interagir com um elemento, primeiro precisamos **encontrá-lo**!

### Tipos de Localizadores

```python
from selenium.webdriver.common.by import By

# 1. Por ID (MAIS COMUM)
_BOTAO_SALVAR = (By.ID, "btnSalvar")

# 2. Por Nome
_CAMPO_EMAIL = (By.NAME, "email")

# 3. Por Classe CSS
_MENSAGEM_ERRO = (By.CLASS_NAME, "error-message")

# 4. Por CSS Selector
_TABELA_RESULTADOS = (By.CSS_SELECTOR, "table.resultados tbody")

# 5. Por XPATH
_LINK_QUITACAO = (By.XPATH, "//a[contains(., 'Quitação')]")

# 6. Por Texto do Link
_LINK_VOLTAR = (By.LINK_TEXT, "Voltar")

# 7. Por Texto Parcial
_LINK_AJUDA = (By.PARTIAL_LINK_TEXT, "Ajuda")

# 8. Por Tag
_TODOS_BOTOES = (By.TAG_NAME, "button")
```

### Qual Usar?

```
ID          → Primeira opção (mais confiável)
CSS         → Segunda opção (rápido e flexível)
XPATH       → Quando os outros não funcionam
CLASS_NAME  → Para estilos CSS
```

### Exemplos do Framework

```python
class PaginaGestaoContratos(PaginaBase):
    # Por ID - mais simples
    _CAMPO_DROPDOWN_SITUACAO = (By.ID, "situacaoContratual")
    
    # Por XPATH - quando precisa ser específico
    _BOTAO_PESQUISAR = (By.XPATH, "//button[contains(., 'Pesquisar')]")
    
    # Por CSS - para tabelas
    _CORPO_TABELA = (By.CSS_SELECTOR, "tbody.mdc-data-table__content")
```

## ⏰ Esperas - Aguardar Elementos

A página web demora para carregar. Precisamos **esperar**!

### Espera Implícita (Automática)

```python
# Definida UMA vez, vale para TODOS os elementos
driver.implicitly_wait(10)  # Espera até 10 segundos

# Agora TODOS os find_element esperam automaticamente
botao = driver.find_element(By.ID, "btnSalvar")
```

**No framework:**
```python
# Já configurado automaticamente no environment.py
# Valor vem do .env: TIMEOUT_IMPLICITO=10
```

### Espera Explícita (Específica)

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Esperar até elemento estar clicável
wait = WebDriverWait(driver, 10)
botao = wait.until(EC.element_to_be_clickable((By.ID, "btnSalvar")))
botao.click()
```

**No framework:**
```python
# Já está encapsulado nos métodos!
# Quando você chama:
self.clicar_no_elemento(self._BOTAO)

# Por trás, o framework já faz:
# - Espera elemento aparecer
# - Espera estar visível
# - Espera estar clicável
# Só então clica!
```

## 🔄 Fluxo Completo de Interação

```python
# 1. Definir localizador
_CAMPO_NOME = (By.ID, "nome")
_BOTAO_SALVAR = (By.ID, "btnSalvar")
_LABEL_SUCESSO = (By.CLASS_NAME, "success-message")

# 2. Preencher campo
self.preencher_campo_texto(self._CAMPO_NOME, "João Silva")

# 3. Clicar botão
self.clicar_no_elemento(self._BOTAO_SALVAR)

# 4. Ler mensagem
mensagem = self.obter_texto_do_elemento(self._LABEL_SUCESSO)

# 5. Validar
assert "Sucesso" in mensagem
```

## 🎯 Exercícios Práticos

### Exercício 1: Identificar Localizadores

Dada essa página HTML, identifique os localizadores:

```html
<input id="cpf" name="cpfCliente" class="form-control" />
<button id="btnPesquisar">Pesquisar</button>
<div class="result-message">Registro encontrado</div>
```

**Solução:**
```python
_CAMPO_CPF = (By.ID, "cpf")
# ou (By.NAME, "cpfCliente")
# ou (By.CLASS_NAME, "form-control")

_BOTAO_PESQUISAR = (By.ID, "btnPesquisar")

_MENSAGEM_RESULTADO = (By.CLASS_NAME, "result-message")
```

### Exercício 2: Sequência de Ações

```python
# Crie uma classe que:
# 1. Preenche nome
# 2. Preenche CPF
# 3. Clica em Salvar
# 4. Lê mensagem de sucesso

class PaginaCadastro(PaginaBase):
    _CAMPO_NOME = (By.ID, "nome")
    _CAMPO_CPF = (By.ID, "cpf")
    _BOTAO_SALVAR = (By.ID, "btnSalvar")
    _MENSAGEM = (By.CLASS_NAME, "message")
    
    def cadastrar_cliente(self, nome, cpf):
        """Cadastra um cliente completo"""
        # 1. Preencher
        self.preencher_campo_texto(self._CAMPO_NOME, nome)
        self.preencher_campo_texto(self._CAMPO_CPF, cpf)
        
        # 2. Salvar
        self.clicar_no_elemento(self._BOTAO_SALVAR)
        
        # 3. Ler mensagem
        mensagem = self.obter_texto_do_elemento(self._MENSAGEM)
        
        return mensagem
```

### Exercício 3: Validação

```python
# Crie um método que valida se um CPF está correto na tela

def validar_cpf_exibido(self, cpf_esperado):
    """Valida se o CPF correto está na tela"""
    # 1. Ler CPF da tela
    cpf_na_tela = self.obter_texto_do_elemento(self._CAMPO_CPF)
    
    # 2. Comparar
    if cpf_na_tela == cpf_esperado:
        print("[OK] CPF correto")
        return True
    else:
        print(f"[ERRO] CPF errado. Esperado: {cpf_esperado}, Tela: {cpf_na_tela}")
        return False
```

## 🔍 Exemplo Completo: Login no ServeRest

### Page Object REAL e EXECUTÁVEL

Este é um Page Object **real** que você pode executar agora mesmo!

**Arquivo:** `pages/exemplos/login_serverest_page.py`

```python
from selenium.webdriver.common.by import By
from pages.base_page import PaginaBase


class PaginaLoginServeRest(PaginaBase):
    """Página de Login do ServeRest - EXEMPLO REAL"""
    
    URL_PAGINA = "https://front.serverest.dev/login"
    
    # LOCALIZADORES (do site real!)
    CAMPO_EMAIL = (By.ID, "email")
    CAMPO_SENHA = (By.ID, "password")
    BOTAO_ENTRAR = (By.CSS_SELECTOR, "button[data-testid='entrar']")
    LINK_CADASTRESE = (By.CSS_SELECTOR, "a[data-testid='cadastrar']")
    
    def __init__(self, driver, configuracao):
        super().__init__(driver)
        self.configuracao = configuracao
    
    def fazer_login(self, usuario, senha):
        """Realiza login no sistema"""
        # 1. PREENCHER usuário
        self.preencher_campo_texto(self._CAMPO_USUARIO, usuario)
        
        # 2. PREENCHER senha
        self.preencher_campo_texto(self._CAMPO_SENHA, senha)
        
        # 3. CLICAR em entrar
        self.clicar_no_elemento(self._BOTAO_ENTRAR)
        
        print(f"[LOGIN] Tentativa com usuário: {usuario}")
    
    def verificar_erro_login(self):
        """Verifica se há mensagem de erro"""
        # 4. LER mensagem (se existir)
        if self.elemento_esta_visivel(self._MENSAGEM_ERRO):
            erro = self.obter_texto_do_elemento(self._MENSAGEM_ERRO)
            return erro
        return None
```

### Step Definition

```python
@when('eu faço login com usuário "{usuario}" e senha "{senha}"')
def fazer_login(context, usuario, senha):
    """Faz login no sistema"""
    context.pagina_login = PaginaLogin(context.driver, context.configuracao)
    context.pagina_login.fazer_login(usuario, senha)


@then('vejo mensagem de erro "{mensagem_esperada}"')
def validar_erro(context, mensagem_esperada):
    """Valida mensagem de erro"""
    erro = context.pagina_login.verificar_erro_login()
    
    assert erro == mensagem_esperada, \
        f"Mensagem errada. Esperado: {mensagem_esperada}, Encontrado: {erro}"
```

## 🎨 Resumo Visual

```
Página Web
    ↓
┌─────────────────────┐
│ [Input Nome    ]    │ ← PREENCHER (send_keys)
│ [Input CPF     ]    │ ← LIMPAR (clear) + PREENCHER
│ [Button Salvar]     │ ← CLICAR (click)
│ Mensagem: Sucesso   │ ← LER (text)
└─────────────────────┘
    ↓
Selenium + Python
    ↓
✅ Teste Automatizado
```

## 💡 Dicas Importantes

### ✅ Sempre Espere

```python
# ❌ Não faça assim (muito rápido)
botao = driver.find_element(By.ID, "btn")
botao.click()  # Pode dar erro se não carregou

# ✅ Faça assim (com espera)
self.clicar_no_elemento(self._BOTAO)  # Framework espera automaticamente
```

### ✅ Sempre Limpe Antes de Preencher

```python
# ❌ Não faça assim
campo.send_keys("João")  # Se já tinha texto, vai concatenar

# ✅ Faça assim
campo.clear()  # Limpa primeiro
campo.send_keys("João")  # Agora preenche limpo

# ✅ Ou use o método do framework (já faz tudo)
self.preencher_campo_texto(localizador, "João")
```

### ✅ Valide Sempre que Ler

```python
# ✅ Leia e valide
cpf = self.obter_texto_do_elemento(self._CAMPO_CPF)

if not cpf:
    print("[ERRO] CPF não encontrado")
else:
    print(f"[OK] CPF: {cpf}")
```

## 🎓 Conceitos-Chave

| Ação | Método Selenium | Método Framework | Quando Usar |
|------|----------------|------------------|-------------|
| Clicar | `element.click()` | `clicar_no_elemento()` | Botões, links, menus |
| Preencher | `element.send_keys()` | `preencher_campo_texto()` | Inputs, textareas |
| Limpar | `element.clear()` | (dentro do preencher) | Antes de digitar |
| Ler | `element.text` | `obter_texto_do_elemento()` | Validações, labels |

## 🔄 Fluxo Típico de um Teste

```python
# 1. ACESSAR página
self.driver.get("https://sistema.com/cadastro")

# 2. PREENCHER formulário
self.preencher_campo_texto(self._CAMPO_NOME, "João")
self.preencher_campo_texto(self._CAMPO_CPF, "123.456.789-00")

# 3. CLICAR em salvar
self.clicar_no_elemento(self._BOTAO_SALVAR)

# 4. LER resultado
mensagem = self.obter_texto_do_elemento(self._MENSAGEM_SUCESSO)

# 5. VALIDAR
assert "Sucesso" in mensagem
```

## 🎯 Exercícios Finais

### Exercício 1: Criar Page Object Simples

Crie uma classe para uma página de busca que tem:
- Campo de texto para busca
- Botão Pesquisar  
- Label com total de resultados

```python
class PaginaBusca(PaginaBase):
    _CAMPO_BUSCA = (By.ID, "search")
    _BOTAO_PESQUISAR = (By.ID, "btnSearch")
    _TOTAL_RESULTADOS = (By.CLASS_NAME, "total-results")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def buscar(self, termo):
        """Realiza uma busca"""
        self.preencher_campo_texto(self._CAMPO_BUSCA, termo)
        self.clicar_no_elemento(self._BOTAO_PESQUISAR)
    
    def obter_total_resultados(self):
        """Lê quantos resultados foram encontrados"""
        total = self.obter_texto_do_elemento(self._TOTAL_RESULTADOS)
        return total
```

### Exercício 2: Usar o Page Object

```python
# Criar página
pagina = PaginaBusca(driver)

# Buscar
pagina.buscar("Python")

# Ler resultado
total = pagina.obter_total_resultados()
print(f"Encontrados: {total} resultados")
```

## 🎮 PRATIQUE AGORA! Exemplo Executável

**Você pode executar este exemplo AGORA MESMO no ServeRest!**

```bash
# No terminal (com venv ativado):
behave features/exemplos/login_serverest.feature --tags=@login
```

Este comando vai:
1. Abrir o navegador Chrome
2. Acessar https://front.serverest.dev/login
3. Verificar que todos os elementos estão visíveis
4. Fechar o navegador

**Experimente!** É de graça e não precisa cadastro! 🚀

Os Page Objects do ServeRest estão em: `pages/exemplos/`

---

## ➡️ Próximo Passo

Você já sabe os 4 pilares! Agora aprenda técnicas avançadas:

**[04_Automacao_Web_Avancado.md](04_Automacao_Web_Avancado.md)** - Dropdowns, Tabelas e mais!

---

**Tempo estimado**: 40 minutos  
**Pré-requisito**: 02_Python_Metodos_Classes.md  
**Próximo**: Automação Web Avançado  
**Site de prática**: 🌐 https://front.serverest.dev

