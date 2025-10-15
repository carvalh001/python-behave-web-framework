# 🚀 Automação Web - Conceitos Avançados

> 💡 **LEITURA FACILITADA**: Use **`Ctrl + Shift + V`** para visualizar formatado!  
> Muito mais fácil de ler! 

Aprenda técnicas avançadas para lidar com elementos complexos da web.

## 📋 Dropdowns (Select)

Dropdowns são campos de seleção com opções pré-definidas.

### Como Funciona

```html
<!-- HTML de um dropdown -->
<select id="estado">
    <option value="SP">São Paulo</option>
    <option value="RJ">Rio de Janeiro</option>
    <option value="MG">Minas Gerais</option>
</select>
```

### Código Puro (Selenium)

```python
from selenium.webdriver.support.ui import Select

# 1. Encontrar o elemento select
elemento_select = driver.find_element(By.ID, "estado")

# 2. Criar objeto Select
select = Select(elemento_select)

# 3. Selecionar por texto visível
select.select_by_visible_text("São Paulo")

# Ou selecionar por valor
select.select_by_value("SP")

# Ou selecionar por índice
select.select_by_index(0)  # Primeira opção
```

### No Framework (PaginaBase)

```python
# Muito mais simples!
_DROPDOWN_ESTADO = (By.ID, "estado")

self.selecionar_opcao_dropdown(self._DROPDOWN_ESTADO, "São Paulo")
```

### Exemplo Completo do Framework

```python
class PaginaRenegociacao(PaginaBase):
    _DROPDOWN_FORMA_PAGAMENTO = (By.ID, "formaPagamento")
    _DROPDOWN_STATUS = (By.ID, "statusRenegociacao")
    
    def selecionar_forma_de_pagamento(self, forma_pagamento):
        """Seleciona forma de pagamento no dropdown"""
        self.selecionar_opcao_dropdown(
            self._DROPDOWN_FORMA_PAGAMENTO,
            forma_pagamento
        )
        print(f"[FORMULÁRIO] Forma: {forma_pagamento}")
    
    def selecionar_status(self, status):
        """Seleciona status no dropdown"""
        self.selecionar_opcao_dropdown(
            self._DROPDOWN_STATUS,
            status
        )
        print(f"[FILTRO] Status: {status}")
```

**No Step:**
```python
@when('eu seleciono a forma de pagamento "{forma}"')
def selecionar_forma(context, forma):
    """Seleciona forma de pagamento"""
    context.pagina.selecionar_forma_de_pagamento(forma)
```

## 📊 Tabelas Dinâmicas

Tabelas contêm múltiplas linhas e colunas. Precisamos navegar por elas!

### Estrutura HTML de Tabela

```html
<table>
    <tbody>
        <tr>  <!-- Linha 1 -->
            <td class="cpf">123.456.789-00</td>
            <td class="nome">João Silva</td>
            <td class="status">Ativo</td>
        </tr>
        <tr>  <!-- Linha 2 -->
            <td class="cpf">987.654.321-00</td>
            <td class="nome">Maria Santos</td>
            <td class="status">Inativo</td>
        </tr>
    </tbody>
</table>
```

### Ler Todas as Linhas

```python
# Código Selenium
linhas = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

for linha in linhas:
    cpf = linha.find_element(By.CSS_SELECTOR, "td.cpf").text
    nome = linha.find_element(By.CSS_SELECTOR, "td.nome").text
    status = linha.find_element(By.CSS_SELECTOR, "td.status").text
    
    print(f"CPF: {cpf}, Nome: {nome}, Status: {status}")
```

### Buscar Linha Específica

```python
# Encontrar linha com CPF específico
def encontrar_linha_por_cpf(self, cpf_procurado):
    """Busca uma linha da tabela pelo CPF"""
    todas_linhas = self._encontrar_elementos(self._LINHAS_TABELA)
    
    for linha in todas_linhas:
        cpf_celula = linha.find_element(By.CSS_SELECTOR, "td.cpf").text
        
        if cpf_celula == cpf_procurado:
            print(f"[OK] Linha encontrada: CPF {cpf_procurado}")
            return linha
    
    print(f"[ERRO] CPF {cpf_procurado} não encontrado")
    return None
```

### Exemplo Real do Framework

```python
class PaginaRenegociacao(PaginaBase):
    _TODAS_LINHAS = (By.CSS_SELECTOR, "tbody tr.mat-mdc-row")
    
    def buscar_opcao_na_tabela(self, prazo, prestacao, taxas):
        """Busca opção específica nas linhas da tabela"""
        todas_linhas = self._encontrar_elementos(self._TODAS_LINHAS)
        
        for linha in todas_linhas:
            # Ler cada coluna
            prazo_celula = linha.find_element(By.CSS_SELECTOR, "td.prazo").text
            prestacao_celula = linha.find_element(By.CSS_SELECTOR, "td.prestacao").text
            taxas_celula = linha.find_element(By.CSS_SELECTOR, "td.taxas").text
            
            # Comparar
            if (prazo_celula == prazo and 
                prestacao in prestacao_celula and 
                taxas in taxas_celula):
                print("[VALIDACAO] [OK] Opção encontrada!")
                return True
        
        return False
```

## 🎯 Localizadores Dinâmicos

Às vezes o localizador muda baseado em dados do teste!

### Conceito

```python
# Localizador FIXO
_BOTAO_SALVAR = (By.ID, "btnSalvar")

# Localizador DINÂMICO - muda baseado em variável
def obter_localizador_linha_cpf(cpf):
    return (By.XPATH, f"//tr[contains(., '{cpf}')]")
```

### Exemplo Real

```python
def abrir_menu_por_cpf(self, cpf_cliente):
    """Abre menu de um CPF específico"""
    # Localizador dinâmico - busca linha com este CPF
    localizador_menu = (
        By.XPATH,
        f"//tr[contains(., '{cpf_cliente}')]//button[@aria-haspopup='menu']"
    )
    
    print(f"[AÇÃO] Abrindo menu para CPF: {cpf_cliente}")
    self.clicar_no_elemento(localizador_menu)
```

### Quando Usar

✅ **Use localizadores dinâmicos quando:**
- Precisar buscar por CPF, nome, ID específico
- Trabalhar com tabelas onde cada linha é diferente
- Elementos têm IDs gerados dinamicamente

```python
# Exemplos
f"//tr[contains(., '{cpf}')]"           # Linha com CPF
f"//button[@data-id='{id_registro}']"   # Botão com ID
f"//td[text()='{nome_cliente}']"        # Célula com nome
```

## ⚠️ Tratamento de Erros

Às vezes elementos não aparecem. Precisamos tratar!

### Try/Except

```python
# Tentar fazer algo, se der erro, fazer outra coisa
try:
    botao = driver.find_element(By.ID, "btnSalvar")
    botao.click()
    print("[OK] Botão clicado")
except:
    print("[ERRO] Botão não encontrado")
```

### Try/Except Específico

```python
from selenium.common.exceptions import TimeoutException

try:
    elemento = self._encontrar_elemento(self._BOTAO)
    elemento.click()
except TimeoutException:
    print("[ERRO] Elemento não apareceu no tempo limite")
except Exception as erro:
    print(f"[ERRO] Erro inesperado: {erro}")
```

### No Framework

```python
def buscar_opcao_na_tabela(self, prazo):
    """Busca opção tratando possíveis erros"""
    linhas = self._encontrar_elementos(self._TODAS_LINHAS)
    
    for linha in linhas:
        try:
            # Tenta ler a célula
            prazo_celula = linha.find_element(By.CSS_SELECTOR, "td.prazo").text
            
            if prazo_celula == prazo:
                return True
        except Exception:
            # Se der erro nesta linha, pula para próxima
            continue
    
    return False
```

## 🔄 Esperas Customizadas

Às vezes precisamos esperar condições específicas!

### Esperar Texto Aparecer

```python
from selenium.webdriver.support import expected_conditions as EC

# Esperar até elemento ter texto
wait = WebDriverWait(driver, 10)
wait.until(lambda driver: elemento.text.strip() != "")
```

**No framework:**
```python
# Já está encapsulado!
texto = self.obter_texto_do_elemento(
    self._CAMPO_CPF,
    aguardar_texto_aparecer=True  # Espera ter texto
)
```

### Esperar Elemento Desaparecer

```python
# Esperar loading sumir
wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading")))
```

## 🎨 Padrão Completo: Page Object Avançado

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from project_lib.pages.base_page import PaginaBase
import time


class PaginaRenegociacao(PaginaBase):
    """Página de Renegociação - Exemplo Avançado"""
    
    # LOCALIZADORES
    _CAMPO_CPF = (By.ID, "cpf")
    _DROPDOWN_STATUS = (By.ID, "statusRenegociacao")
    _BOTAO_PESQUISAR = (By.XPATH, "//button[text()='Pesquisar']")
    _TABELA_RESULTADOS = (By.CSS_SELECTOR, "tbody tr")
    _BOTAO_EDITAR_PRIMEIRA_LINHA = (By.CSS_SELECTOR, "tbody tr:first-child button.editar")
    
    def __init__(self, driver, configuracao):
        super().__init__(driver)
        self.configuracao = configuracao
        self.url_pagina = configuracao.url_renegociacao
    
    def carregar_pagina(self):
        """Navega para a página"""
        self.driver.get(self.url_pagina)
        print(f"[PÁGINA] Renegociação carregada")
    
    def buscar_renegociacao(self, cpf, status):
        """Busca completa - COMBINA várias ações"""
        # 1. Preencher CPF
        self.preencher_campo_texto(self._CAMPO_CPF, cpf)
        
        # 2. Selecionar status no dropdown
        self.selecionar_opcao_dropdown(self._DROPDOWN_STATUS, status)
        
        # 3. Clicar pesquisar
        self.clicar_no_elemento(self._BOTAO_PESQUISAR)
        
        # 4. Aguardar resultados
        time.sleep(1)
        
        print(f"[BUSCA] CPF: {cpf}, Status: {status}")
    
    def clicar_editar_primeira_renegociacao(self):
        """Clica em editar na primeira linha da tabela"""
        self.clicar_no_elemento(self._BOTAO_EDITAR_PRIMEIRA_LINHA)
        time.sleep(2)  # Aguarda formulário carregar
        print("[AÇÃO] Primeira renegociação aberta")
    
    def contar_resultados(self):
        """Conta quantas linhas foram encontradas"""
        linhas = self._encontrar_elementos(self._TABELA_RESULTADOS)
        total = len(linhas)
        print(f"[RESULTADO] {total} registro(s) encontrado(s)")
        return total
```

## 🎯 Exercícios Finais

### Exercício 1: Trabalhar com Dropdown

```python
# Crie método que seleciona uma cidade em um dropdown
_DROPDOWN_CIDADE = (By.ID, "cidade")

def selecionar_cidade(self, nome_cidade):
    """Seleciona cidade no dropdown"""
    self.selecionar_opcao_dropdown(self._DROPDOWN_CIDADE, nome_cidade)
    print(f"[FILTRO] Cidade: {nome_cidade}")
```

### Exercício 2: Buscar em Tabela

```python
# Crie método que busca um cliente pelo nome na tabela
def buscar_cliente_por_nome(self, nome_procurado):
    """Busca cliente na tabela pelo nome"""
    todas_linhas = self._encontrar_elementos(self._LINHAS_TABELA)
    
    for linha in todas_linhas:
        nome_celula = linha.find_element(By.CSS_SELECTOR, "td.nome").text
        
        if nome_celula == nome_procurado:
            print(f"[OK] Cliente {nome_procurado} encontrado")
            return linha
    
    print(f"[ERRO] Cliente {nome_procurado} não encontrado")
    return None
```

### Exercício 3: Localizador Dinâmico

```python
# Crie método que clica no botão "Editar" de um contrato específico
def clicar_editar_contrato(self, numero_contrato):
    """Clica em editar de um contrato específico"""
    localizador = (
        By.XPATH,
        f"//tr[contains(., '{numero_contrato}')]//button[text()='Editar']"
    )
    self.clicar_no_elemento(localizador)
    print(f"[AÇÃO] Editando contrato: {numero_contrato}")
```

## 💡 Dicas Avançadas

### 1. Aguardar Conteúdo Dinâmico

```python
# Quando a tabela carrega dinamicamente
def aguardar_tabela_carregar(self):
    """Espera a tabela ter conteúdo"""
    time.sleep(1)  # Pequena espera
    linhas = self._encontrar_elementos(self._LINHAS_TABELA)
    
    if len(linhas) > 0:
        print(f"[OK] Tabela carregada com {len(linhas)} linha(s)")
    else:
        print("[AVISO] Tabela vazia")
```

### 2. Lidar com Múltiplas Janelas

```python
# Salvar janela original
janela_original = driver.current_window_handle

# Clicar em link que abre nova aba
self.clicar_no_elemento(self._LINK_NOVA_ABA)

# Trocar para nova janela
for janela in driver.window_handles:
    if janela != janela_original:
        driver.switch_to.window(janela)
        break

# Voltar para janela original
driver.switch_to.window(janela_original)
```

### 3. Scroll na Página

```python
# Scroll até o final
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Scroll até elemento
elemento = driver.find_element(By.ID, "rodape")
driver.execute_script("arguments[0].scrollIntoView();", elemento)
```

## 🎯 Padrões do Framework

### 1. Nomenclatura de Localizadores

```python
# Seja específico no nome!
_BOTAO_SALVAR                    # Botão
_CAMPO_INPUT_NOME                # Campo de input
_CAMPO_DROPDOWN_STATUS           # Dropdown
_TABELA_RESULTADOS               # Tabela inteira
_LINHAS_TABELA_RESULTADOS        # Linhas da tabela
_PRIMEIRA_LINHA                  # Linha específica
_COLUNA_CPF                      # Coluna específica
_LINK_VOLTAR                     # Link
_LABEL_MENSAGEM_SUCESSO          # Label/texto
```

### 2. Métodos Compostos

Combine ações para criar fluxos completos:

```python
def preencher_formulario_completo(self, dados):
    """Preenche todos os campos do formulário"""
    self.preencher_campo_texto(self._CAMPO_NOME, dados['nome'])
    self.preencher_campo_texto(self._CAMPO_CPF, dados['cpf'])
    self.preencher_campo_texto(self._CAMPO_EMAIL, dados['email'])
    self.selecionar_opcao_dropdown(self._DROPDOWN_ESTADO, dados['estado'])
    print("[FORMULÁRIO] Todos os campos preenchidos")

def buscar_e_editar(self, cpf):
    """Busca um registro e abre para edição"""
    self.preencher_campo_texto(self._CAMPO_BUSCA, cpf)
    self.clicar_no_elemento(self._BOTAO_PESQUISAR)
    self.clicar_no_elemento(self._BOTAO_EDITAR_PRIMEIRA_LINHA)
    print(f"[AÇÃO] Registro {cpf} aberto para edição")
```

### 3. Validações Robustas

```python
def validar_dados_completos(self, dados_esperados):
    """Valida múltiplos campos de uma vez"""
    erros = []
    
    # Ler todos os campos
    nome_tela = self.obter_texto_do_elemento(self._LABEL_NOME)
    cpf_tela = self.obter_texto_do_elemento(self._LABEL_CPF)
    status_tela = self.obter_texto_do_elemento(self._LABEL_STATUS)
    
    # Validar cada um
    if nome_tela != dados_esperados['nome']:
        erros.append(f"Nome incorreto: {nome_tela}")
    
    if cpf_tela != dados_esperados['cpf']:
        erros.append(f"CPF incorreto: {cpf_tela}")
    
    if status_tela != dados_esperados['status']:
        erros.append(f"Status incorreto: {status_tela}")
    
    # Se houver erros, falha o teste
    if erros:
        raise AssertionError("\n".join(erros))
    
    print("[VALIDACAO] [OK] Todos os dados corretos")
```

## 📚 Resumo de Técnicas

| Técnica | Quando Usar | Exemplo |
|---------|-------------|---------|
| Dropdown | Campos de seleção | Estados, status, formas de pagamento |
| Tabelas | Múltiplos registros | Lista de contratos, clientes |
| Localizador Dinâmico | Buscar elemento específico | Linha com CPF X, botão do registro Y |
| Try/Except | Lidar com erros | Elemento opcional, pode não existir |
| Time.sleep | Aguardar carregamento | Após clicar, após salvar |
| For loop | Percorrer lista | Cada linha da tabela |

## 🎯 Exercício Final Completo

Crie um Page Object para uma tela de consulta de contratos:

```python
from selenium.webdriver.common.by import By
from project_lib.pages.base_page import PaginaBase


class PaginaConsultaContratos(PaginaBase):
    """Página de Consulta de Contratos"""
    
    # Localizadores
    _CAMPO_CPF_FILTRO = (By.ID, "cpfFiltro")
    _DROPDOWN_SITUACAO = (By.ID, "situacao")
    _BOTAO_PESQUISAR = (By.ID, "btnPesquisar")
    _TABELA_LINHAS = (By.CSS_SELECTOR, "tbody tr")
    
    def __init__(self, driver, configuracao):
        super().__init__(driver)
        self.configuracao = configuracao
    
    def pesquisar_por_cpf_e_situacao(self, cpf, situacao):
        """Busca contratos por CPF e situação"""
        # Preencher filtros
        self.preencher_campo_texto(self._CAMPO_CPF_FILTRO, cpf)
        self.selecionar_opcao_dropdown(self._DROPDOWN_SITUACAO, situacao)
        
        # Pesquisar
        self.clicar_no_elemento(self._BOTAO_PESQUISAR)
        
        print(f"[BUSCA] CPF: {cpf}, Situação: {situacao}")
    
    def obter_total_contratos_encontrados(self):
        """Conta quantos contratos foram encontrados"""
        linhas = self._encontrar_elementos(self._TABELA_LINHAS)
        return len(linhas)
    
    def clicar_no_contrato_numero(self, numero_contrato):
        """Clica em um contrato específico pelo número"""
        localizador = (
            By.XPATH,
            f"//tr[contains(., '{numero_contrato}')]//button[@class='view']"
        )
        self.clicar_no_elemento(localizador)
        print(f"[AÇÃO] Contrato {numero_contrato} aberto")
```

**Step usando tudo isso:**
```python
@when('eu busco contratos do CPF "{cpf}" com situação "{situacao}"')
def buscar_contratos(context, cpf, situacao):
    """Busca contratos"""
    context.pagina.pesquisar_por_cpf_e_situacao(cpf, situacao)
    
    total = context.pagina.obter_total_contratos_encontrados()
    print(f"[RESULTADO] {total} contrato(s) encontrado(s)")
```

## ➡️ Próximo Passo

Agora você domina as técnicas! Aprenda a integrar tudo no framework:

**[05_Integrando_Com_Framework.md](05_Integrando_Com_Framework.md)** - Conectando Feature → Step → Page!

---

**Tempo estimado**: 50 minutos  
**Pré-requisito**: 03_Automacao_Web_Basico.md  
**Próximo**: Integração com Framework

