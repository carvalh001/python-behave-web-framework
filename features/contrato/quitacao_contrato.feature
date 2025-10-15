# language: pt
Funcionalidade: Quitação de Contrato
  Como um usuário do sistema
  Eu quero consultar um contrato com situação "Normal"
  Para acessar a tela de detalhes de quitação

  @regressivo @quitacao @teste
  Cenário: Visualizar detalhes da quitação de um contrato com situação "Normal"    
    Dado que um contrato com situação "Normal" foi gerado para o cliente de CPF "015.107.737-11"
    
    E eu acesso a tela de Gestão de Contratos
    Quando eu preencho o filtro "Situação Contratual" com o valor "Normal" e clico em "Pesquisar"
    E eu aciono a opção "Quitação" no menu de ações do contrato com CPF "015.107.737-11"    
    
    Então a tela de "Quitação" é exibida com os dados do CPF "015.107.737-11"

