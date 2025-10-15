from recursos.utils.gerenciador_configuracao import GerenciadorDeConfiguracao
from recursos.utils.gerenciador_navegador import GerenciadorDeNavegador
from recursos.utils.gerenciador_evidencias import GerenciadorDeEvidencias
from recursos.utils.gerenciador_relatorio import GerenciadorDeRelatorio


def before_all(context):
    """
    Executado UMA vez antes de todos os testes.
    Inicializa configurações, preparar ambiente e coletar informações do sistema.
    """
    print("\n" + "="*60)
    print("INICIANDO EXECUÇÃO DOS TESTES")
    print("="*60 + "\n")
    
    context.configuracao = GerenciadorDeConfiguracao()
    
    context.gerenciador_relatorio = GerenciadorDeRelatorio(context.configuracao)
    context.gerenciador_relatorio.registrar_inicio_execucao()
    
    context.gerenciador_evidencias = GerenciadorDeEvidencias(context.configuracao)
    context.gerenciador_evidencias.preparar_diretorios()


def before_scenario(context, scenario):
    """
    Executado ANTES de cada cenário individual.
    Inicializa o navegador, prepara evidências e inicia gravação de vídeo.
    """
    print(f"\n{'-'*60}")
    print(f"CENARIO: {scenario.name}")
    print(f"{'-'*60}\n")
    
    context.gerenciador_navegador = GerenciadorDeNavegador(context.configuracao)
    context.driver = context.gerenciador_navegador.inicializar_navegador()
    
    if not hasattr(context, 'informacoes_navegador_coletadas'):
        informacoes_navegador = context.gerenciador_navegador.obter_informacoes()
        context.gerenciador_relatorio.registrar_informacoes_navegador(informacoes_navegador)
        context.informacoes_navegador_coletadas = True
    
    context.gerenciador_evidencias.iniciar_contagem_passos()
    context.gerenciador_evidencias.iniciar_gravacao_video(context.driver, scenario.name)


def after_step(context, step):
    """
    Executado APÓS cada passo (step).
    Captura screenshot automaticamente se o passo falhar.
    """
    if step.status in ["failed", "error"]:
        nome_arquivo_screenshot = context.gerenciador_evidencias.capturar_screenshot_falha(
            context.driver,
            step.name
        )
        
        if nome_arquivo_screenshot and not hasattr(step, 'screenshots'):
            step.screenshots = []
            step.screenshots.append(nome_arquivo_screenshot)


def after_scenario(context, scenario):
    """
    Executado APÓS cada cenário.
    Finaliza gravação de vídeo e fecha o navegador.
    """
    print(f"\n{'-'*60}")
    print(f"CENARIO FINALIZADO: {scenario.name}")
    print(f"STATUS: {scenario.status}")
    print(f"{'-'*60}\n")
    
    cenario_falhou = (scenario.status == 'failed')
    tem_tag_video_always = any(tag == 'video_always' for tag in scenario.tags)
    
    nome_video = context.gerenciador_evidencias.finalizar_gravacao_video(
        cenario_falhou,
        tem_tag_video_always
    )
    
    if nome_video:
        scenario.video_file = nome_video
    
    context.gerenciador_navegador.fechar_navegador()


def after_all(context):
    """
    Executado UMA vez após todos os testes.
    Finaliza execução, salva metadados e exibe resumo.
    """
    context.gerenciador_relatorio.registrar_fim_execucao()
    context.gerenciador_relatorio.salvar_metadados()
    
    resumo = context.gerenciador_relatorio.obter_resumo_execucao()
    
    print("\n" + "="*60)
    print("RESUMO DA EXECUÇÃO")
    print("="*60)
    print(f"Início:    {resumo['inicio']}")
    print(f"Término:   {resumo['fim']}")
    print(f"Duração:   {resumo['duracao']}")
    print(f"Sistema:   {resumo['sistema']}")
    print(f"Navegador: {resumo['navegador']}")
    print("="*60 + "\n")
