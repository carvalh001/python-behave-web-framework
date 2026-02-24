# language: pt
Funcionalidade: Autenticação no Portal de Colaboradores
  Como um usuário do portal
  Eu quero fazer login com meu perfil
  Para acessar as funcionalidades do sistema

  @portal @autenticacao @login
  Cenário: Acessar tela de login do Portal
    Dado que estou na página de login do Portal de Colaboradores
    Então vejo o campo de usuário ou e-mail
    E vejo o campo de senha na tela de login
    E vejo o botão Entrar na tela de login

  @portal @autenticacao @login
  Esquema do Cenário: Login com cada perfil do sistema
    Dado que estou na página de login do Portal de Colaboradores
    Quando eu preencho o usuário "<usuario>" no Portal
    E eu preencho a senha "<senha>" no Portal
    E eu clico no botão Entrar do Portal
    Então sou redirecionado para a página inicial do Portal
    E vejo a área logada do Portal

    Exemplos:
      | perfil        | usuario | senha    |
      | Colaborador   | maria   | 123456   |
      | Gestor RH     | joao    | 123456   |
      | Admin         | admin   | admin123 |
