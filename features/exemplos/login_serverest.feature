# language: pt
Funcionalidade: Login no ServeRest
  Como um usuário
  Eu quero fazer login no sistema ServeRest
  Para acessar as funcionalidades

  @exemplo @serverest @login
  Cenário: Acessar tela de login
    Dado que estou na página de login do ServeRest
    Então vejo o campo de email
    E vejo o campo de senha
    E vejo o botão Entrar

  @exemplo @serverest @cadastro
  Cenário: Navegar para cadastro
    Dado que estou na página de login do ServeRest
    Quando eu clico no link Cadastre-se
    Então sou redirecionado para a página de cadastro

