# Testes do Portal de Colaboradores

Testes de automação para o frontend **Portal de Colaboradores**, usando o mesmo padrão do framework (Behave, Page Objects, steps em português).

## Pré-requisitos

1. **Backend** (`portal-colaborador-backend`) rodando, com banco populado (seed com usuários de teste).
2. **Frontend** (`portal-colaboradores`) rodando (ex.: `npm run dev` — geralmente em `http://localhost:5173`).
3. No `.env` do framework, definir a URL do frontend:
   ```env
   URL_BASE_SISTEMA=http://localhost:5173
   ```

## Executando os testes de autenticação

```bash
# Todos os cenários do Portal (inclui autenticação)
behave features/portal/ -f pretty

# Apenas a feature de autenticação
behave features/portal/autenticacao.feature -f pretty

# Por tag (ex.: só logins)
behave features/portal/ --tags=@portal
behave features/portal/ --tags=@login
behave features/portal/ --tags=@admin
```

## Perfis de teste (credenciais do seed)

| Perfil      | Usuário | Senha   | Tag        |
|------------|---------|---------|------------|
| Colaborador | maria   | 123456  | @colaborador |
| Gestor RH   | joao    | 123456  | @gestor_rh   |
| Admin      | admin   | admin123| @admin       |

## Estrutura criada

- **Feature:** `features/portal/autenticacao.feature` — cenários de tela de login e login com os três perfis.
- **Steps:** `features/steps/portal_auth_steps.py` — passos reutilizáveis para login no Portal.
- **Page Object:** `pages/portal/login_portal_page.py` — página de login (campos e ações).

Os cenários seguem o padrão do framework: `Dado/Quando/Então`, Page Object com seletores centralizados e uso de `context.configuracao.url_base_sistema` para a URL base.
