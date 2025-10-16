# Screenshots do Último Passo

## Visão Geral

O framework agora suporta **três modos de captura de screenshots**:

1. **Screenshots em falhas** - Captura quando um passo falha (padrão)
2. **Screenshots em todos os passos** - Captura em cada passo do cenário
3. **Screenshot no último passo** - Captura apenas no último passo de cada cenário ⭐ **NOVO**

## Configuração

### Variável de Ambiente

Adicione no arquivo `.env`:

```env
# Captura screenshot apenas no ÚLTIMO passo de cada cenário
# (independente de sucesso ou falha)
SCREENSHOT_ULTIMO_PASSO=true
```

### Valores Aceitos

- `true`, `yes`, `1`, `sim`, `verdadeiro` → Habilita
- `false`, `no`, `0`, `não`, `falso` → Desabilita (padrão)

## Quando Usar

### ✅ Use Screenshot no Último Passo quando:

- Você quer uma **evidência final** de cada cenário sem sobrecarregar com muitas imagens
- Precisa comprovar que o cenário chegou até o fim
- Quer ter uma captura do **estado final** da aplicação após todos os passos
- Deseja evidências tanto de **cenários que passam quanto que falham**

### ❌ NÃO use quando:

- Você precisa evidência de **cada passo individual** (use `SCREENSHOT_EM_TODOS_PASSOS=true`)
- Quer apenas screenshots de **falhas** (use apenas `SCREENSHOT_EM_FALHAS=true`)
- Está preocupado com espaço em disco (desabilite tudo)

## Comparação dos Modos

| Modo | Quando Captura | Quantidade de Imagens | Uso Recomendado |
|------|---------------|----------------------|-----------------|
| **Em Falhas** | Apenas quando falha | Baixa | Debugging de erros |
| **Todos os Passos** | Cada passo | Alta (muitas imagens) | Auditoria completa |
| **Último Passo** | Último passo do cenário | Média (1 por cenário) | Evidência final balanceada |

## Nomenclatura dos Arquivos

Os screenshots do último passo seguem o padrão:

```
ultimo_passo_{timestamp}_{nome_cenario}_{nome_passo}.png
```

**Exemplo:**
```
ultimo_passo_20251016_152535_032434_Calcular_novas_opcoes_para_uma_renegociacao_existe_E_uma_opcao_com_prazo_de_12_meses.png
```

## Exemplos de Configuração

### Exemplo 1: Apenas Evidência Final

```env
SCREENSHOT_EM_FALHAS=false
SCREENSHOT_EM_TODOS_PASSOS=false
SCREENSHOT_ULTIMO_PASSO=true
```

✅ **Resultado**: 1 screenshot por cenário (estado final)

### Exemplo 2: Falhas + Evidência Final

```env
SCREENSHOT_EM_FALHAS=true
SCREENSHOT_EM_TODOS_PASSOS=false
SCREENSHOT_ULTIMO_PASSO=true
```

✅ **Resultado**: Screenshots de falhas + 1 screenshot final de cada cenário

### Exemplo 3: Auditoria Completa

```env
SCREENSHOT_EM_FALHAS=true
SCREENSHOT_EM_TODOS_PASSOS=true
SCREENSHOT_ULTIMO_PASSO=false
```

✅ **Resultado**: Screenshot de cada passo (incluindo falhas)

### Exemplo 4: Mínimo (Padrão)

```env
SCREENSHOT_EM_FALHAS=true
SCREENSHOT_EM_TODOS_PASSOS=false
SCREENSHOT_ULTIMO_PASSO=false
```

✅ **Resultado**: Apenas screenshots de passos que falharam

## Como Funciona Internamente

1. **Before Scenario**: Framework registra o cenário atual e inicia contagem de passos
2. **After Each Step**: Incrementa contador e verifica:
   - Se o passo falhou → Captura screenshot (se `SCREENSHOT_EM_FALHAS=true`)
   - Se é o último passo → Captura screenshot (se `SCREENSHOT_ULTIMO_PASSO=true`)
3. **Detecção do Último Passo**: Compara `índice_atual == total_passos`

## Integração com Relatórios

Os screenshots do último passo são **automaticamente incluídos** no relatório HTML, junto com:

- Screenshots de falhas
- Vídeos de evidência
- Logs de execução

## Dicas de Uso

### 💡 Dica 1: Combinação Ideal para Regressão

```env
SCREENSHOT_EM_FALHAS=true
SCREENSHOT_ULTIMO_PASSO=true
GRAVAR_VIDEO_SEMPRE=false
```

**Por quê?** Você terá evidência visual de cada cenário sem sobrecarregar com muitas imagens, e vídeos apenas de falhas.

### 💡 Dica 2: Economia de Espaço

Se você tem muitos cenários (>50), considere:

```env
SCREENSHOT_ULTIMO_PASSO=false
GRAVAR_VIDEO_SEMPRE=false
```

E use apenas vídeos em falhas como evidência.

### 💡 Dica 3: Demonstração/Apresentação

Para criar uma apresentação visual dos testes:

```env
SCREENSHOT_ULTIMO_PASSO=true
GRAVAR_VIDEO_SEMPRE=true
```

Você terá screenshots finais + vídeos completos de todos os cenários.

## Troubleshooting

### Problema: Screenshots não estão sendo capturados

**Soluções:**

1. Verifique se `SCREENSHOT_ULTIMO_PASSO=true` está no arquivo `.env`
2. Confirme que o arquivo `.env` está na raiz do projeto
3. Verifique se o navegador está acessível (não feche antes do último passo)
4. Veja os logs do terminal para mensagens de erro

### Problema: Muitos screenshots sendo gerados

**Solução:**

Você provavelmente tem múltiplos modos habilitados:

```env
# Desabilite os que não precisa
SCREENSHOT_EM_TODOS_PASSOS=false
SCREENSHOT_ULTIMO_PASSO=true  # Mantenha apenas este
```

### Problema: Screenshot vazio ou em branco

**Causa**: O navegador pode estar em modo headless e a página não carregou completamente.

**Solução**:

```env
TIMEOUT_CONTEUDO_DINAMICO=3  # Aumenta timeout
```

## Referências

- 📄 [02_REFERENCIA_METODOS.md](02_REFERENCIA_METODOS.md) - Métodos do framework
- 📄 [04_SCREENSHOTS_EXEMPLO.md](04_SCREENSHOTS_EXEMPLO.md) - Exemplos de screenshots
- 📄 [env.example](../env.example) - Arquivo de configuração exemplo

---

**Última atualização**: 16/10/2025  
**Versão do Framework**: 1.1.0

