import os, sys
sys.stdout.reconfigure(encoding='utf-8')

out_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\minimalist_subs_bloco2"
os.makedirs(out_dir, exist_ok=True)

HEADER = """\
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,54,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,80,80,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(s):
    h = int(s//3600); m = int((s%3600)//60); sec = s%60
    return f"{h}:{m:02d}:{sec:05.2f}"

def line(s, e, text):
    return f"Dialogue: 0,{ts(s)},{ts(e)},Default,,0,0,0,,{text}\n"

subs = {}

# V01 — O problema não era cobrar R$300
# Segmento 1: 45:14-45:53 (39s) + Segmento 2: 47:54-48:06 (12s)
# Relative: seg1=0-39, then seg2=39-51
subs["b2_v01.ass"] = HEADER + \
    line(0,   4,   "Cliente muito barato é o cara mais chato...") + \
    line(4,   9,   "Porque ele quer controlar sua vida inteira") + \
    line(9,  14,   "por um trabalho de R$300 ou R$400.") + \
    line(14, 18,   "Só que eu acho que o problema não é isso.") + \
    line(18, 22,   "O problema é fechar sem deixar claro") + \
    line(22, 27,   "o que está incluído no serviço.") + \
    line(27, 32,   "Um pacote de R$300 pode funcionar muito bem") + \
    line(32, 37,   "se você definir: quantas entregas,") + \
    line(37, 42,   "quantas alterações, prazo, canal de atendimento.") + \
    line(42, 47,   "Porque quando nada está definido...") + \
    line(47, 52,   "o cliente acha que contratou sua disponibilidade infinita.")

# V02 — Eu amo trabalhar, mas odeio ser controlada
# Segmento: 48:12-49:14 (62s)
subs["b2_v02.ass"] = HEADER + \
    line(0,   5,   "Eu estou trabalhando igual uma maluca...") + \
    line(5,  10,   "mas tenho fé que, quando acabar essa automatização,") + \
    line(10, 15,   "vou conseguir trabalhar um pouco menos.") + \
    line(15, 20,   "Mas provavelmente vou criar outro projeto.") + \
    line(20, 25,   "Porque eu acordo querendo ver novidades,") + \
    line(25, 30,   "querendo programar, querendo pesquisar.") + \
    line(30, 35,   "Eu acho que eu gosto mesmo de trabalhar.") + \
    line(35, 42,   "O que eu não gosto é ser cobrada\\Npor uma coisa que eu sei que estou fazendo.") + \
    line(42, 48,   "Outra pessoa controlando minha rotina") + \
    line(48, 55,   "por um trabalho que eu já sei que vai sair.") + \
    line(55, 62,   "Isso me desgasta. Não é o trabalho em si.")

# V03 — Por que sistemas em nuvem são caros?
# Segmento 1: 39:36-40:12 (36s) pular 40:12-40:18, retomar 40:18-40:40 (22s) = 58s total
subs["b2_v03.ass"] = HEADER + \
    line(0,   5,   "Eu tive que fazer isso para um sistema meu...") + \
    line(5,  10,   "e só aí entendi por que é tão caro.") + \
    line(10, 15,   "Eu precisava conectar vários quiosques de shopping.") + \
    line(15, 20,   "Todos dependiam do mesmo sistema de estoque.") + \
    line(20, 26,   "Qualquer falha obrigava a equipe a conferir\\Nos estoques do zero.") + \
    line(26, 32,   "Você não paga apenas pelo código.") + \
    line(32, 38,   "Você paga pelo monitoramento, pela segurança,") + \
    line(38, 44,   "pela recuperação quando algo falha,") + \
    line(44, 50,   "pela consistência dos dados.") + \
    line(50, 58,   "A responsabilidade e o estresse foram\\Nnum nível que eu nem sei explicar.")

# V04 — O medo de lançar está me atrasando
# Segmento 1: 44:38-45:14 (36s) + 46:06-46:20 (14s) + 47:00-47:20 (20s) = 70s total
subs["b2_v04.ass"] = HEADER + \
    line(0,   6,   "Eu já poderia ter lançado alguma coisa\\Nfaz muito tempo.") + \
    line(6,  12,   "Só que eu quero construir uma empresa escalável.") + \
    line(12, 18,   "Quero entregar algo bom desde o início.") + \
    line(18, 24,   "Não quero decepcionar ninguém.") + \
    line(24, 30,   "Mas eu sempre encontro uma parte que poderia melhorar.") + \
    line(30, 36,   "Sempre quero fazer algo maior, algo diferente.") + \
    line(36, 42,   "E aí acabo trabalhando demais\\Nem coisas que ainda não existem.") + \
    line(42, 50,   "Meu desafio não é ter ideias nem começar.") + \
    line(50, 60,   "É aceitar quando uma primeira versão\\Njá está boa o suficiente para existir.") + \
    line(60, 70,   "Mas eu não consigo entregar algo meia-boca.\\NE sei que isso pode me prejudicar.")

# V05 — O sistema que estou construindo
# Segmento 1: 42:32-43:14 (42s) + 49:28-49:52 (24s) = 66s total
subs["b2_v05.ass"] = HEADER + \
    line(0,   6,   "Eu estou fazendo uma plataforma\\Nde social media criada com IA.") + \
    line(6,  13,   "A empresa manda os dados dela.") + \
    line(13, 20,   "O sistema cria posts e vídeos\\Npara os próximos 30 dias.") + \
    line(20, 26,   "O objetivo é entregar isso em aproximadamente 24 horas.") + \
    line(26, 34,   "O desafio não é gerar conteúdo.") + \
    line(34, 42,   "É fazer algo automático que não tenha\\Ncara de IA e que ainda fique bonito.") + \
    line(42, 50,   "Você não sabe como é difícil fazer algo automático") + \
    line(50, 58,   "que respeite a identidade da marca.") + \
    line(58, 66,   "O objetivo não é gerar mais conteúdo.\\NÉ gerar conteúdo que faça sentido.")

# V06 — Como estudar vídeos virais sem copiar
# Segmento 1: 50:04-50:18 (14s) pular 50:18-50:32, retomar 50:32-51:16 (44s) = 58s total
subs["b2_v06.ass"] = HEADER + \
    line(0,   7,   "Eu uso APIs para encontrar os vídeos\\Nque mais viralizaram no nicho.") + \
    line(7,  14,   "O sistema analisa estrutura, tema e roteiro.") + \
    line(14, 20,   "Mas o objetivo não é copiar.") + \
    line(20, 27,   "É entender o gancho, o ritmo, o formato.") + \
    line(27, 34,   "O que fez aquele vídeo performar?") + \
    line(34, 40,   "E como adaptar isso para outro nicho,\\Noutra empresa, outro contexto?") + \
    line(40, 47,   "Copiar um viral não é estratégia.") + \
    line(47, 52,   "Entender o padrão e criar algo original...") + \
    line(52, 58,   "isso sim é diferencial.")

# V07 — Antes de criar um aplicativo, faça isso
# Segmento: 1:00:10-1:00:46 (36s)
subs["b2_v07.ass"] = HEADER + \
    line(0,   5,   "Alguém perguntou: aplicativo para melhorar fotos\\Npara o público feminino é uma boa ideia?") + \
    line(5,  11,   "A primeira coisa que você tem que fazer") + \
    line(11, 16,   "é estudar o mercado.") + \
    line(16, 22,   "Já existe uma solução parecida?") + \
    line(22, 27,   "Quanto ela custa? Quem usa?") + \
    line(27, 32,   "O que os usuários reclamam?") + \
    line(32, 36,   "Com quem você vai competir?")

# RESERVA 1 — Nunca trabalhei CLT
# Segmento: 31:58-32:48 (50s)
subs["b2_r01.ass"] = HEADER + \
    line(0,   6,   "Eu nunca trabalhei com carteira assinada.") + \
    line(6,  12,   "Sempre trabalhei com clientes, projetos, liberdade.") + \
    line(12, 18,   "Mas existe uma insegurança que aparece às vezes.") + \
    line(18, 26,   "O que acontece se minha empresa não der certo?") + \
    line(26, 32,   "E eu precisar entrar no mercado formal\\Nsem experiência CLT?") + \
    line(32, 40,   "Essa dúvida aparece de vez em quando.") + \
    line(40, 50,   "Empreender também é conviver com ela.")

# RESERVA 2 — O erro de segurança
# Segmento 1: 1:01:18-1:01:26 (8s) + 1:01:30-1:01:48 (18s) = 26s total
subs["b2_r02.ass"] = HEADER + \
    line(0,   5,   "Hoje eu peço para o agente pesquisar\\Ne deixo ele instalar...") + \
    line(5,  11,   "Mas eu sei que isso pode trazer vírus.") + \
    line(11, 17,   "Eu já tive Discord e Instagram invadidos.") + \
    line(17, 22,   "A autenticação em dois fatores ajudou na recuperação.") + \
    line(22, 26,   "Mas ela não substitui prevenção.")

for fname, content in subs.items():
    path = os.path.join(out_dir, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {fname}")

print("\nAll 9 subtitle files created!")
