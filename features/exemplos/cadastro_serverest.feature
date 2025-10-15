# language: pt
Funcionalidade: Cadastro de Usuário no ServeRest
  Como um novo usuário
  Eu quero me cadastrar no sistema ServeRest
  Para poder usar as funcionalidades

  @exemplo @serverest @cadastro
  Cenário: Acessar tela de cadastro
    Dado que estou na página de cadastro do ServeRest
    Então vejo o campo de nome
    E vejo o campo de email
    E vejo o campo de senha
    E vejo o checkbox de administrador
    E vejo o botão Cadastrar

