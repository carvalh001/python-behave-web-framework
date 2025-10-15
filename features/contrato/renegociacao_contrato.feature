# language: pt
Funcionalidade: Renegociação de Contrato
  Como um usuário do sistema
  Eu quero recalcular as condições de uma renegociação existente
  Para visualizar as novas opções de parcelamento

  @regressivo @renegociacao @calculo @e2e @video_always
  Cenário: Calcular novas opções para uma renegociação existente
    # Acessar a tela de Renegociação
    Dado que eu estou na tela de "Renegociação de Contrato"
    
    # Buscar renegociação por filtros (sem pré-condição de massa de dados)
    Quando eu preencho o CPF "000.061.801-24" no filtro de pesquisa
    E eu seleciono o status "Calculada" no filtro
    E eu clico no botão "Pesquisar"
    
    # Editar a primeira renegociação encontrada
    E eu clico no botão "Editar" da primeira renegociação da lista
    
    # Preencher formulário de renegociação com datas dinâmicas
    E eu preencho a data de referência com o dia posterior ao corrente
    E eu preencho a data do primeiro vencimento com 1 mês e 2 dias a partir do dia corrente
    E eu seleciono a forma de pagamento "Pix"
    E eu preencho a margem consignável com "150,00"
    E eu preencho a prestação com "1,40"
    E eu preencho o prazo com "12"
    E eu preencho a taxa de juros com "1,72"
    E eu limpo o campo "Desconto"
    E eu limpo o campo "Entrada de Renegociação"
    E eu limpo o campo "Data Entrada"
    
    # Executar o cálculo
    Quando eu clico no botão "Calcular"
    
    # Verificações das opções de parcelamento
    Então a tabela de opções de parcelamento é exibida
    E uma opção com prazo de "12" meses, prestação de "R$ 1,30" e taxas de "R$ 1,74" está disponível