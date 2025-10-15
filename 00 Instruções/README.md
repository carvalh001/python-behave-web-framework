# 🎓 Instruções - Tutorial Python e Automação Web

> 💡 **DICA IMPORTANTE**: Pressione **`Ctrl + Shift + V`** para visualizar este documento formatado!  
> Facilita muito a leitura! 📖✨

**Bem-vindo!** Esta pasta contém tutoriais completos para quem **nunca programou em Python** ou **nunca fez automação web**.

## 🎯 Para Quem É Este Tutorial?

- ✅ **Iniciantes totais** em programação
- ✅ **Analistas de teste** que querem aprender automação
- ✅ Quem conhece **teste manual** e quer automatizar
- ✅ Profissionais mudando de carreira para QA

**Não precisa saber nada de programação!** Vamos ensinar do zero.

---

## 📚 Trilha de Aprendizado

Siga esta ordem para melhor aproveitamento:

### 🟢 Módulo 1: Fundamentos Python (2-3 horas)

#### 01. [Variáveis e Listas](01_Python_Variaveis_Listas.md)
- ⏱️ Tempo: 30-40 minutos
- 📝 Conteúdo: Tipos de variáveis, listas, loops FOR e WHILE
- 🎯 Objetivo: Entender estruturas básicas do Python
- 💡 Ao final você saberá: Criar variáveis, trabalhar com listas, fazer loops

#### 02. [Métodos e Classes](02_Python_Metodos_Classes.md)
- ⏱️ Tempo: 45-60 minutos
- 📝 Conteúdo: Funções, classes, objetos, herança
- 🎯 Objetivo: Dominar Orientação a Objetos
- 💡 Ao final você saberá: Criar classes, métodos, usar herança

### 🟡 Módulo 2: Automação Web (3-4 horas)

#### 03. [Automação Web - Básico](03_Automacao_Web_Basico.md)
- ⏱️ Tempo: 40-50 minutos
- 📝 Conteúdo: Os 4 pilares (click, send_keys, clear, text)
- 🎯 Objetivo: Saber interagir com páginas web
- 💡 Ao final você saberá: Clicar, preencher, limpar e ler elementos

#### 04. [Automação Web - Avançado](04_Automacao_Web_Avancado.md)
- ⏱️ Tempo: 50-60 minutos
- 📝 Conteúdo: Dropdowns, tabelas, localizadores dinâmicos
- 🎯 Objetivo: Técnicas avançadas de automação
- 💡 Ao final você saberá: Trabalhar com elementos complexos

### 🔵 Módulo 3: Framework BDD (2-3 horas)

#### 05. [Integrando com Framework](05_Integrando_Com_Framework.md)
- ⏱️ Tempo: 60-90 minutos
- 📝 Conteúdo: Feature → Step → Page, padrão completo
- 🎯 Objetivo: Conectar tudo no framework
- 💡 Ao final você saberá: Criar testes completos no framework

#### 06. [Próximos Passos](06_Proximos_Passos.md)
- ⏱️ Tempo: 30 minutos
- 📝 Conteúdo: Checklist, exercícios, próxima jornada
- 🎯 Objetivo: Consolidar conhecimento e evoluir
- 💡 Ao final você saberá: Onde ir a partir daqui

---

## ⏰ Tempo Total Estimado

- **Leitura**: 4-6 horas
- **Prática/Exercícios**: 3-4 horas
- **Total**: 7-10 horas

**Sugestão:** Dedique 1-2 horas por dia durante uma semana.

---

## 🎯 Roteiros Sugeridos

### Para Quem Nunca Programou

```
Dia 1: 01_Python_Variaveis_Listas.md (fazer TODOS exercícios)
Dia 2: 02_Python_Metodos_Classes.md (fazer TODOS exercícios)
Dia 3: 03_Automacao_Web_Basico.md
Dia 4: 04_Automacao_Web_Avancado.md
Dia 5: 05_Integrando_Com_Framework.md
Dia 6: Criar seu primeiro teste!
Dia 7: 06_Proximos_Passos.md + revisar tudo
```

### Para Quem Sabe Python Básico

```
Dia 1: Revisar 01 e 02 (rápido) + fazer 03
Dia 2: 04_Automacao_Web_Avancado.md
Dia 3: 05_Integrando_Com_Framework.md
Dia 4: Criar 2-3 testes
Dia 5: Explorar Docs/ avançado
```

### Para Quem Já Fez Automação

```
1h: Ler 05_Integrando_Com_Framework.md
1h: Ler Docs/03_BOAS_PRATICAS.md
2h: Criar testes seguindo padrões do framework
```

---

## 💡 Dicas de Estudo

### ✅ Faça

1. **Digite os códigos** (não copie/cole)
2. **Faça TODOS os exercícios**
3. **Experimente modificar** os exemplos
4. **Peça ajuda** quando travar
5. **Pratique diariamente** (mesmo que 30 min)

### ❌ Evite

1. Apenas ler sem praticar
2. Pular exercícios
3. Copiar código sem entender
4. Desistir no primeiro erro
5. Estudar apenas teoria

### 🎯 Método Eficaz

```
1. LER o conceito
2. VER o exemplo
3. DIGITAR o código
4. MODIFICAR e experimentar
5. FAZER o exercício
6. ENSINAR para alguém (melhor forma de fixar!)
```

---

## 🆘 Precisa de Ajuda?

### Durante o Estudo

- **Não entendi um conceito?** → Releia devagar, busque no Google
- **Erro no código?** → Leia a mensagem de erro, verifique linha por linha
- **Travou em exercício?** → Tente de outra forma, consulte exemplos

### Perguntas Frequentes

**P: Quanto tempo para dominar?**
R: Com dedicação, 2-4 semanas para básico, 2-3 meses para avançado.

**P: Preciso decorar tudo?**
R: Não! Entenda os conceitos. Consulte a documentação quando precisar.

**P: E se eu errar muito?**
R: Normal! Erro faz parte do aprendizado. Analise o erro, corrija, aprenda.

**P: Qual a melhor forma de praticar?**
R: Criar testes reais para o sistema. Comece simples, evolua gradualmente.

---

## 🎁 Bônus: Comandos Úteis

```bash
# Ativar ambiente virtual
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar todos os testes
behave

# Executar teste específico
behave features/contrato/quitacao_contrato.feature

# Executar com tag
behave --tags=@quitacao

# Ver ajuda
behave --help

# Python interativo (para testar códigos)
python
>>> nome = "João"
>>> print(nome)
>>> exit()
```

---

## 📍 Após Completar Este Tutorial

### Você Estará Pronto Para:

✅ Criar testes automatizados  
✅ Trabalhar com Page Objects  
✅ Escrever Features em Gherkin  
✅ Implementar Steps  
✅ Usar o framework com confiança  
✅ Ajudar outros iniciantes  

### Próximos Passos:

1. 🚀 **Começar a criar testes reais**
2. 📚 **Explorar [Docs/](../Docs/)** - Documentação avançada
3. 🔍 **Estudar código existente** do framework
4. 🤝 **Colaborar com o time**
5. 📈 **Evoluir continuamente**

---

## 🏆 Seu Progresso

Marque conforme completar:

- [ ] ✅ Completei 01_Python_Variaveis_Listas.md
- [ ] ✅ Completei 02_Python_Metodos_Classes.md
- [ ] ✅ Completei 03_Automacao_Web_Basico.md
- [ ] ✅ Completei 04_Automacao_Web_Avancado.md
- [ ] ✅ Completei 05_Integrando_Com_Framework.md
- [ ] ✅ Completei 06_Proximos_Passos.md
- [ ] 🎯 Criei meu primeiro teste
- [ ] 🎯 Criei 5+ testes
- [ ] 🎯 Ajudei um colega
- [ ] 🎯 Me sinto confiante!

---

## 📞 Contato

**Dúvidas ou sugestões?**
- Entre em contato com a equipe de QA
- Compartilhe seu feedback
- Ajude a melhorar este material

---

**Vamos começar?** Abra o [01_Python_Variaveis_Listas.md](01_Python_Variaveis_Listas.md) e boa jornada! 🚀

---

**Organização**: Assert Consulting  
**Framework**: Siepex v2.0  
**Atualizado**: Outubro 2025

