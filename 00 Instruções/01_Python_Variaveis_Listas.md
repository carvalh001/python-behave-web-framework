# 🐍 Python Básico - Variáveis e Listas

> 💡 **DICA**: Pressione **`Ctrl + Shift + V`** para ver este documento formatado!  
> Muito mais fácil de ler! 

Bem-vindo ao mundo da programação! Este guia vai te ensinar os fundamentos do Python de forma simples e prática.

## 📝 O Que São Variáveis?

Variáveis são como "caixas" onde guardamos informações que vamos usar no código.

### Tipos de Variáveis

#### 1. Texto (String)
```python
# Textos sempre entre aspas (simples ou duplas)
nome = "João Silva"
cpf = "123.456.789-00"
mensagem = 'Teste realizado com sucesso'

# Usar o valor da variável
print(nome)  # Exibe: João Silva
print(f"CPF do cliente: {cpf}")  # Exibe: CPF do cliente: 123.456.789-00
```

**No framework:**
```python
# Em um Page Object
def preencher_campo_nome(self, nome_cliente):
    """Preenche o campo nome"""
    self.preencher_campo_texto(self._CAMPO_NOME, nome_cliente)
    print(f"[FORMULÁRIO] Nome: {nome_cliente}")
```

#### 2. Números Inteiros (Int)
```python
# Números sem casas decimais
idade = 25
quantidade_meses = 12
timeout = 10

# Operações matemáticas
total = quantidade_meses * 2  # total = 24
resultado = idade + 5  # resultado = 30
```

**No framework:**
```python
# Configurações de timeout
timeout_implicito = 10
timeout_explicito = 15

self.driver.implicitly_wait(timeout_implicito)
```

#### 3. Números Decimais (Float)
```python
# Números com casas decimais
taxa_juros = 1.72
valor_prestacao = 150.50
margem = 1500.00

# Operações
total = valor_prestacao * 12  # total = 1806.0
```

**No framework:**
```python
# Em um Step
def preencher_taxa_juros(context, valor):
    """Preenche a taxa de juros"""
    context.pagina.preencher_campo_taxa_juros(valor)
```

#### 4. Verdadeiro/Falso (Boolean)
```python
# Apenas dois valores possíveis: True ou False
teste_passou = True
navegador_headless = False
elemento_visivel = True

# Usado em condições
if teste_passou:
    print("Sucesso!")
else:
    print("Falhou")
```

**No framework:**
```python
# Verificações
if self.elemento_esta_visivel(self._BOTAO_SALVAR):
    print("Botão encontrado")
    return True
else:
    print("Botão não encontrado")
    return False
```

## 📋 Listas

Listas armazenam **múltiplos valores** em uma única variável.

### Criando Listas
```python
# Lista vazia
clientes = []

# Lista com valores
cpfs = ["123.456.789-00", "987.654.321-00", "111.222.333-44"]
idades = [25, 30, 45, 18]
nomes = ["João", "Maria", "Pedro"]

# Lista mista (pode, mas evite)
misturado = ["João", 25, True, 150.50]
```

### Acessando Elementos
```python
cpfs = ["123.456.789-00", "987.654.321-00", "111.222.333-44"]

# Índices começam em 0!
primeiro_cpf = cpfs[0]    # "123.456.789-00"
segundo_cpf = cpfs[1]     # "987.654.321-00"
ultimo_cpf = cpfs[-1]     # "111.222.333-44" (último)

print(primeiro_cpf)
```

**No framework:**
```python
# Buscar em tabela
todas_linhas = self._encontrar_elementos(self._LINHAS_TABELA)
primeira_linha = todas_linhas[0]  # Pega a primeira linha
```

### Manipulando Listas
```python
# Adicionar elemento
nomes = ["João"]
nomes.append("Maria")      # nomes = ["João", "Maria"]
nomes.append("Pedro")      # nomes = ["João", "Maria", "Pedro"]

# Remover elemento
nomes.remove("Maria")      # nomes = ["João", "Pedro"]

# Tamanho da lista
quantidade = len(nomes)    # quantidade = 2

# Verificar se existe
existe = "João" in nomes   # existe = True
```

**No framework:**
```python
# Coletar todos os valores de uma coluna
valores_prestacao = []
for linha in todas_linhas:
    valor = linha.find_element(By.CSS_SELECTOR, "td.prestacao").text
    valores_prestacao.append(valor)

print(f"Total de opções: {len(valores_prestacao)}")
```

## 🔁 Loop FOR

O `for` repete ações **para cada** elemento de uma lista.

### Sintaxe Básica
```python
# Para cada nome na lista de nomes
nomes = ["João", "Maria", "Pedro"]

for nome in nomes:
    print(f"Olá, {nome}!")

# Resultado:
# Olá, João!
# Olá, Maria!
# Olá, Pedro!
```

### Com Números
```python
# Loop de 0 a 4 (5 não incluso)
for numero in range(5):
    print(numero)

# Resultado: 0, 1, 2, 3, 4

# Loop de 1 a 10
for numero in range(1, 11):
    print(numero)

# Resultado: 1, 2, 3, ... 10
```

**No framework:**
```python
# Percorrer todas as linhas de uma tabela
todas_linhas = self._encontrar_elementos(self._LINHAS_TABELA)

for linha in todas_linhas:
    cpf = linha.find_element(By.CSS_SELECTOR, "td.cpf").text
    status = linha.find_element(By.CSS_SELECTOR, "td.status").text
    print(f"CPF: {cpf}, Status: {status}")
```

### Exemplo Real do Framework
```python
def buscar_opcao_na_tabela(self, prazo_esperado, prestacao_esperada):
    """Busca uma opção específica na tabela"""
    todas_linhas = self._encontrar_elementos(self._TODAS_OPCOES)
    
    for linha in todas_linhas:
        prazo = linha.find_element(By.CSS_SELECTOR, "td.prazo").text
        prestacao = linha.find_element(By.CSS_SELECTOR, "td.prestacao").text
        
        if prazo == prazo_esperado and prestacao == prestacao_esperada:
            print(f"[OK] Opção encontrada!")
            return True
    
    return False  # Não encontrou
```

## 🔄 Loop WHILE

O `while` repete **enquanto** uma condição for verdadeira.

### Sintaxe Básica
```python
# Contador
contador = 0

while contador < 5:
    print(f"Contagem: {contador}")
    contador = contador + 1  # Incrementa

# Resultado: 0, 1, 2, 3, 4
```

### Com Condições
```python
# Tentar até conseguir
tentativas = 0
sucesso = False

while tentativas < 3 and not sucesso:
    print(f"Tentativa {tentativas + 1}")
    # Simula tentativa
    tentativas = tentativas + 1
    if tentativas == 2:
        sucesso = True
        print("Conseguiu!")
```

**No framework:**
```python
# Tentar obter texto com retry
def obter_texto_com_retentativa(self, localizador, tentativas_maximas=3):
    """Tenta obter texto múltiplas vezes"""
    tentativa_atual = 0
    
    while tentativa_atual < tentativas_maximas:
        elemento = self._encontrar_elemento(localizador)
        texto = elemento.text.strip()
        
        if texto:  # Se tem texto, retorna
            return texto
        
        tentativa_atual = tentativa_atual + 1
        time.sleep(1)  # Aguarda 1 segundo
    
    return ""  # Não conseguiu
```

## 🎯 Exercícios Práticos

### Exercício 1: Variáveis
```python
# Declare variáveis para armazenar:
# - Um CPF
# - Uma idade
# - Um valor em dinheiro
# - Se o teste passou ou não

cpf_cliente = "123.456.789-00"
idade_cliente = 30
valor_credito = 15000.50
teste_passou = True

# Agora exiba todas elas
print(f"CPF: {cpf_cliente}")
print(f"Idade: {idade_cliente}")
print(f"Valor: R$ {valor_credito}")
print(f"Passou: {teste_passou}")
```

### Exercício 2: Listas
```python
# Crie uma lista com 3 CPFs
cpfs = ["111.111.111-11", "222.222.222-22", "333.333.333-33"]

# Adicione mais um CPF
cpfs.append("444.444.444-44")

# Exiba quantos CPFs existem
print(f"Total de CPFs: {len(cpfs)}")

# Exiba cada um
for cpf in cpfs:
    print(f"CPF: {cpf}")
```

### Exercício 3: Loop FOR
```python
# Você tem uma lista de status
status_list = ["Ativo", "Inativo", "Pendente", "Cancelado"]

# Use FOR para exibir cada status numerado
for indice, status in enumerate(status_list, start=1):
    print(f"{indice}. {status}")

# Resultado:
# 1. Ativo
# 2. Inativo
# 3. Pendente
# 4. Cancelado
```

### Exercício 4: Loop WHILE
```python
# Simule tentativas de login até 3 vezes
tentativas = 0
logado = False

while tentativas < 3 and not logado:
    print(f"Tentativa de login: {tentativas + 1}")
    
    # Simula login (na 2ª tentativa funciona)
    if tentativas == 1:
        logado = True
        print("Login bem-sucedido!")
    
    tentativas = tentativas + 1

if not logado:
    print("Falha no login após 3 tentativas")
```

## 💡 Dicas Importantes

### ✅ Boas Práticas

1. **Use nomes descritivos**
   ```python
   ✅ nome_cliente = "João"
   ❌ n = "João"
   ```

2. **Evite valores mágicos**
   ```python
   ✅ TENTATIVAS_MAXIMAS = 3
   ✅ while tentativa < TENTATIVAS_MAXIMAS:
   
   ❌ while tentativa < 3:  # O que é 3?
   ```

3. **Comente quando necessário**
   ```python
   # Aguarda 2 segundos para a página carregar
   time.sleep(2)
   ```

### 🎯 Contexto no Framework

Tudo que você aprendeu aqui é usado no framework:

- **Variáveis**: Armazenar CPF, nomes, valores
- **Listas**: Percorrer linhas de tabelas
- **FOR**: Buscar elementos em tabelas
- **WHILE**: Tentativas com retry

## ➡️ Próximo Passo

Agora que você domina variáveis e listas, vá para:

**[02_Python_Metodos_Classes.md](02_Python_Metodos_Classes.md)** - Aprenda sobre métodos e classes!

---

**Tempo estimado**: 30 minutos  
**Pré-requisito**: Nenhum (comece aqui!)  
**Próximo**: Métodos e Classes

