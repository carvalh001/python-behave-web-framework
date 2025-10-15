# 🏗️ Python Básico - Métodos e Classes

> 💡 **DICA**: Pressione **`Ctrl + Shift + V`** para visualizar formatado!  
> Muito mais fácil de ler! 

Aprenda sobre funções, métodos e orientação a objetos de forma simples!

## 🔧 O Que São Métodos (Funções)?

Métodos são **blocos de código reutilizáveis** que executam uma tarefa específica.

### Função Simples

```python
# Definir uma função
def saudar():
    print("Olá, mundo!")

# Chamar a função
saudar()  # Exibe: Olá, mundo!
```

### Função com Parâmetros

```python
# Função que recebe dados
def saudar_pessoa(nome):
    print(f"Olá, {nome}!")

# Chamar passando o nome
saudar_pessoa("João")   # Exibe: Olá, João!
saudar_pessoa("Maria")  # Exibe: Olá, Maria!
```

### Função com Retorno

```python
# Função que calcula e retorna um valor
def somar(numero1, numero2):
    resultado = numero1 + numero2
    return resultado

# Usar o valor retornado
total = somar(10, 5)
print(f"Total: {total}")  # Exibe: Total: 15
```

**No framework:**
```python
# Método que retorna um valor
def obter_cpf_exibido_na_tela(self):
    """Obtém o CPF da tela"""
    cpf = self.obter_texto_do_elemento(self._CAMPO_CPF)
    return cpf

# Usar em um step
cpf_encontrado = context.pagina.obter_cpf_exibido_na_tela()
print(f"CPF: {cpf_encontrado}")
```

### Função com Múltiplos Parâmetros

```python
def calcular_prestacao(valor_total, quantidade_parcelas, taxa_juros):
    """Calcula o valor da prestação"""
    juros = valor_total * (taxa_juros / 100)
    total_com_juros = valor_total + juros
    prestacao = total_com_juros / quantidade_parcelas
    return prestacao

# Usar
valor_prestacao = calcular_prestacao(10000, 12, 2.5)
print(f"Prestação: R$ {valor_prestacao:.2f}")
```

## 🏛️ O Que São Classes?

Classes são **moldes** para criar objetos. Pense em uma classe como uma "receita" e o objeto como o "bolo pronto".

### Classe Simples

```python
# Definir a classe
class Cliente:
    pass  # Classe vazia por enquanto

# Criar um objeto (instância) da classe
cliente1 = Cliente()
cliente2 = Cliente()
```

### Classe com Atributos

```python
class Cliente:
    # Construtor - executa quando criamos o objeto
    def __init__(self, nome, cpf):
        self.nome = nome  # Atributo
        self.cpf = cpf    # Atributo

# Criar clientes
cliente1 = Cliente("João", "123.456.789-00")
cliente2 = Cliente("Maria", "987.654.321-00")

# Acessar atributos
print(cliente1.nome)  # Exibe: João
print(cliente2.cpf)   # Exibe: 987.654.321-00
```

### Classe com Métodos

```python
class Cliente:
    def __init__(self, nome, cpf, saldo):
        self.nome = nome
        self.cpf = cpf
        self.saldo = saldo
    
    def exibir_dados(self):
        """Exibe os dados do cliente"""
        print(f"Nome: {self.nome}")
        print(f"CPF: {self.cpf}")
        print(f"Saldo: R$ {self.saldo:.2f}")
    
    def adicionar_saldo(self, valor):
        """Adiciona valor ao saldo"""
        self.saldo = self.saldo + valor
        print(f"Saldo atualizado: R$ {self.saldo:.2f}")

# Usar a classe
cliente = Cliente("João", "123.456.789-00", 1000.00)
cliente.exibir_dados()
cliente.adicionar_saldo(500.00)
```

**Resultado:**
```
Nome: João
CPF: 123.456.789-00
Saldo: R$ 1000.00
Saldo atualizado: R$ 1500.00
```

## 🎭 Classes no Framework (Page Objects)

No framework, cada **página web** é representada por uma **classe**!

### Exemplo Real: PaginaQuitacao

```python
class PaginaQuitacao(PaginaBase):
    """Página de Quitação de Contrato"""
    
    # Localizadores (atributos da classe)
    _CAMPO_CPF = (By.ID, "cpf")
    _BOTAO_CALCULAR = (By.ID, "btnCalcular")
    
    def __init__(self, driver):
        """Construtor - inicializa a página"""
        super().__init__(driver)  # Chama construtor da classe pai
        self.driver = driver
    
    def obter_cpf_exibido(self):
        """Método - obtém CPF da tela"""
        cpf = self.obter_texto_do_elemento(self._CAMPO_CPF)
        return cpf
    
    def clicar_botao_calcular(self):
        """Método - clica no botão"""
        self.clicar_no_elemento(self._BOTAO_CALCULAR)
```

### Como Usar no Teste

```python
# Criar instância da página
pagina_quitacao = PaginaQuitacao(context.driver)

# Usar os métodos
cpf = pagina_quitacao.obter_cpf_exibido()
print(f"CPF: {cpf}")

pagina_quitacao.clicar_botao_calcular()
```

## 🌳 Herança

Herança permite que uma classe **herde** características de outra.

### Conceito

```python
# Classe pai (base)
class Animal:
    def __init__(self, nome):
        self.nome = nome
    
    def fazer_som(self):
        print("Som genérico")

# Classe filha (herda de Animal)
class Cachorro(Animal):
    def fazer_som(self):
        print("Au au!")

class Gato(Animal):
    def fazer_som(self):
        print("Miau!")

# Usar
rex = Cachorro("Rex")
rex.fazer_som()  # Exibe: Au au!

mimi = Gato("Mimi")
mimi.fazer_som()  # Exibe: Miau!
```

### No Framework: PaginaBase

```python
# Classe PAI - métodos que TODAS as páginas usam
class PaginaBase:
    def __init__(self, driver):
        self.driver = driver
    
    def clicar_no_elemento(self, localizador):
        """Todas as páginas podem clicar"""
        elemento = self._encontrar_elemento(localizador)
        elemento.click()
    
    def preencher_campo_texto(self, localizador, texto):
        """Todas as páginas podem preencher"""
        elemento = self._encontrar_elemento(localizador)
        elemento.clear()
        elemento.send_keys(texto)

# Classe FILHA - herda todos os métodos da PaginaBase
class PaginaGestaoContratos(PaginaBase):
    _BOTAO_PESQUISAR = (By.ID, "btnPesquisar")
    
    def __init__(self, driver):
        super().__init__(driver)  # Chama construtor do pai
    
    def clicar_botao_pesquisar(self):
        # Usa método herdado da PaginaBase!
        self.clicar_no_elemento(self._BOTAO_PESQUISAR)
```

**Vantagem**: Você escreve o método `clicar_no_elemento()` UMA vez na `PaginaBase` e TODAS as páginas podem usar!

## 📦 Self - O Que É Isso?

`self` refere-se ao **próprio objeto**. É como dizer "eu mesmo".

```python
class Pessoa:
    def __init__(self, nome):
        self.nome = nome  # "Meu nome é..."
    
    def apresentar(self):
        print(f"Meu nome é {self.nome}")  # Usa "meu" nome
    
    def mudar_nome(self, novo_nome):
        self.nome = novo_nome  # Muda "meu" nome

# Criar pessoa
pessoa = Pessoa("João")
pessoa.apresentar()  # Meu nome é João

pessoa.mudar_nome("João Silva")
pessoa.apresentar()  # Meu nome é João Silva
```

**No framework:**
```python
class PaginaQuitacao(PaginaBase):
    def __init__(self, driver):
        self.driver = driver  # Guarda o driver como "meu" driver
    
    def obter_cpf(self):
        # Usa "meu" driver para buscar elemento
        elemento = self.driver.find_element(By.ID, "cpf")
        return elemento.text
```

## 🎯 Exercícios Práticos

### Exercício 1: Criar uma Função

```python
# Crie uma função que recebe um CPF e valida se tem 11 dígitos
def validar_cpf(cpf):
    """Valida se CPF tem formato correto"""
    cpf_sem_pontos = cpf.replace(".", "").replace("-", "")
    
    if len(cpf_sem_pontos) == 11:
        return True
    else:
        return False

# Testar
print(validar_cpf("123.456.789-00"))  # True
print(validar_cpf("123"))              # False
```

### Exercício 2: Criar uma Classe

```python
class Contrato:
    def __init__(self, numero, cpf_cliente, valor):
        self.numero = numero
        self.cpf_cliente = cpf_cliente
        self.valor = valor
        self.situacao = "Ativo"
    
    def exibir_resumo(self):
        print(f"Contrato: {self.numero}")
        print(f"Cliente: {self.cpf_cliente}")
        print(f"Valor: R$ {self.valor:.2f}")
        print(f"Situação: {self.situacao}")
    
    def quitar(self):
        self.situacao = "Quitado"
        print("Contrato quitado!")

# Criar e usar
contrato = Contrato("00001-8", "123.456.789-00", 10000.00)
contrato.exibir_resumo()
contrato.quitar()
contrato.exibir_resumo()
```

### Exercício 3: Herança

```python
# Classe base
class Veiculo:
    def __init__(self, marca):
        self.marca = marca
    
    def buzinar(self):
        print("Beep beep!")

# Classe filha
class Carro(Veiculo):
    def __init__(self, marca, modelo):
        super().__init__(marca)  # Chama construtor do pai
        self.modelo = modelo
    
    def exibir_info(self):
        print(f"{self.marca} {self.modelo}")

# Usar
carro = Carro("Toyota", "Corolla")
carro.exibir_info()  # Toyota Corolla
carro.buzinar()      # Beep beep! (herdado)
```

## 🎓 Aplicando no Framework

### Estrutura Típica de um Page Object

```python
from selenium.webdriver.common.by import By
from project_lib.pages.base_page import PaginaBase


class PaginaCadastroCliente(PaginaBase):
    """Página de Cadastro - HERDA de PaginaBase"""
    
    # Localizadores (atributos da classe)
    _CAMPO_NOME = (By.ID, "nome")
    _CAMPO_CPF = (By.ID, "cpf")
    _BOTAO_SALVAR = (By.ID, "btnSalvar")
    
    def __init__(self, driver, configuracao):
        """Construtor"""
        super().__init__(driver)  # Herda da PaginaBase
        self.configuracao = configuracao
    
    def preencher_nome(self, nome):
        """Método específico desta página"""
        # Usa método HERDADO da PaginaBase
        self.preencher_campo_texto(self._CAMPO_NOME, nome)
        print(f"[FORMULÁRIO] Nome: {nome}")
    
    def preencher_cpf(self, cpf):
        """Método específico desta página"""
        # Usa método HERDADO da PaginaBase
        self.preencher_campo_texto(self._CAMPO_CPF, cpf)
        print(f"[FORMULÁRIO] CPF: {cpf}")
    
    def salvar_cadastro(self):
        """Método específico desta página"""
        # Usa método HERDADO da PaginaBase
        self.clicar_no_elemento(self._BOTAO_SALVAR)
        print("[AÇÃO] Cadastro salvo")
```

### Como Usar no Step

```python
from behave import given, when, then

@when('eu preencho o nome "{nome}" e CPF "{cpf}"')
def preencher_dados(context, nome, cpf):
    """Step que usa o Page Object"""
    # Criar objeto da página
    pagina = PaginaCadastroCliente(context.driver, context.configuracao)
    
    # Chamar métodos
    pagina.preencher_nome(nome)
    pagina.preencher_cpf(cpf)
    pagina.salvar_cadastro()
```

## 🔑 Palavras-Chave Importantes

### `def`
Define uma função ou método
```python
def minha_funcao():
    pass
```

### `class`
Define uma classe
```python
class MinhaClasse:
    pass
```

### `__init__`
Construtor - executa ao criar o objeto
```python
def __init__(self, parametro):
    self.atributo = parametro
```

### `self`
Refere-se ao próprio objeto
```python
self.nome = "João"  # Meu nome
self.meu_metodo()   # Meu método
```

### `super()`
Chama métodos da classe pai
```python
super().__init__(driver)  # Chama __init__ do pai
```

### `return`
Retorna um valor da função
```python
return resultado
```

## 📚 Comparação: Antes e Depois

### Sem Classes (Repetitivo)
```python
# Preencher formulário - REPETINDO código
def preencher_formulario_pagina1():
    driver.find_element(By.ID, "nome").send_keys("João")
    driver.find_element(By.ID, "cpf").send_keys("123")

def preencher_formulario_pagina2():
    driver.find_element(By.ID, "nome").send_keys("Maria")
    driver.find_element(By.ID, "cpf").send_keys("456")
```

### Com Classes (Reutilizável)
```python
class PaginaFormulario:
    def __init__(self, driver):
        self.driver = driver
        self._CAMPO_NOME = (By.ID, "nome")
        self._CAMPO_CPF = (By.ID, "cpf")
    
    def preencher_dados(self, nome, cpf):
        """Método reutilizável"""
        self.driver.find_element(*self._CAMPO_NOME).send_keys(nome)
        self.driver.find_element(*self._CAMPO_CPF).send_keys(cpf)

# Usar em qualquer lugar
pagina = PaginaFormulario(driver)
pagina.preencher_dados("João", "123")
pagina.preencher_dados("Maria", "456")
```

## 🎯 Exercícios Práticos

### Exercício 1: Criar Funções

```python
# Crie uma função que converte real para dólar
def converter_real_para_dolar(valor_reais, cotacao_dolar):
    """Converte valor de reais para dólares"""
    valor_dolares = valor_reais / cotacao_dolar
    return valor_dolares

# Testar
dolares = converter_real_para_dolar(5000, 5.20)
print(f"US$ {dolares:.2f}")  # US$ 961.54
```

### Exercício 2: Criar uma Classe

```python
class Calculadora:
    def __init__(self):
        self.historico = []  # Lista de operações
    
    def somar(self, a, b):
        resultado = a + b
        self.historico.append(f"{a} + {b} = {resultado}")
        return resultado
    
    def subtrair(self, a, b):
        resultado = a - b
        self.historico.append(f"{a} - {b} = {resultado}")
        return resultado
    
    def exibir_historico(self):
        print("Histórico de operações:")
        for operacao in self.historico:
            print(f"  {operacao}")

# Usar
calc = Calculadora()
calc.somar(10, 5)
calc.subtrair(20, 8)
calc.exibir_historico()
```

### Exercício 3: Herança

```python
# Classe base
class PaginaBase:
    def __init__(self, driver):
        self.driver = driver
    
    def clicar(self, localizador):
        elemento = self.driver.find_element(*localizador)
        elemento.click()

# Classe filha
class PaginaLogin(PaginaBase):
    _BOTAO_ENTRAR = (By.ID, "btnEntrar")
    
    def __init__(self, driver):
        super().__init__(driver)  # Herda driver
    
    def fazer_login(self):
        # Usa método HERDADO
        self.clicar(self._BOTAO_ENTRAR)

# Usar
pagina = PaginaLogin(driver)
pagina.fazer_login()  # Usa método herdado!
```

## 💡 Conceitos-Chave

### 1. Métodos São Reutilizáveis
✅ Escreva uma vez, use várias vezes
```python
def validar_cpf(cpf):
    return len(cpf.replace(".", "").replace("-", "")) == 11

# Usar em vários lugares
validar_cpf("123.456.789-00")
validar_cpf("987.654.321-00")
```

### 2. Classes Organizam Código
✅ Agrupa dados e comportamentos relacionados
```python
class Contrato:
    # Dados do contrato
    numero, cpf, valor
    
    # Comportamentos do contrato
    calcular_prestacao()
    quitar()
    renegociar()
```

### 3. Herança Evita Duplicação
✅ Métodos comuns ficam na classe pai
```python
PaginaBase:  ← Métodos comuns (clicar, preencher)
    ↓
PaginaQuitacao, PaginaRenegociacao  ← Herdam tudo!
```

## 🎓 Resumo

| Conceito | O Que É | Exemplo |
|----------|---------|---------|
| Função/Método | Bloco de código reutilizável | `def calcular():` |
| Parâmetro | Entrada da função | `def somar(a, b):` |
| Return | Saída da função | `return resultado` |
| Classe | Molde para objetos | `class Cliente:` |
| Objeto | Instância da classe | `cliente = Cliente()` |
| `__init__` | Construtor | `def __init__(self):` |
| `self` | Referência ao objeto | `self.nome` |
| Herança | Classe que herda de outra | `class Filho(Pai):` |
| `super()` | Acessa classe pai | `super().__init__()` |

## ➡️ Próximo Passo

Agora que você entende métodos e classes, aprenda sobre automação web:

**[03_Automacao_Web_Basico.md](03_Automacao_Web_Basico.md)** - Os 4 pilares da automação!

---

**Tempo estimado**: 45 minutos  
**Pré-requisito**: 01_Python_Variaveis_Listas.md  
**Próximo**: Automação Web Básico

