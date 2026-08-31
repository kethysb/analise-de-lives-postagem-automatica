"""
Gera o arquivo de legenda .ass para os 7 novos vídeos do Bloco 3
"""
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_bloco3")
os.makedirs(subs_dir, exist_ok=True)

# Cabeçalho ASS Kinético elegante
ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,58,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,0,2,80,80,360,1
Style: Highlight,Arial,62,&H0000FFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,0,2,80,80,360,1
Style: TitleCard,Arial,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,2,0,2,80,80,1440,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    cs = int((s - int(s)) * 100)
    return f"{h}:{m:02d}:{int(s):02d}.{cs:02d}"

# Legendas personalizadas para cada vídeo do Bloco 3
subs_data = {
    "b3_v01.ass": [
        (0.0, 4.0, "Eu comecei vendendo perfume como freelancer."),
        (4.0, 8.0, "Eu ganhava R$70 por dia no inicio."),
        (8.0, 14.0, "Tenho 20 anos e comecei a trabalhar faz 1 ano."),
        (14.0, 22.0, "Falei com o dono do negocio e apresentei um projeto."),
        (22.0, 30.0, "Fui estudar o negocio dele antes da reuniao."),
        (30.0, 42.0, "As pessoas foram conhecendo meu trabalho e confiadno."),
        (42.0, 52.0, "Foi assim que fui conseguindo meus primeiros clientes."),
        (52.0, 61.0, "Agora minha meta e fazer isso por trafego pago!")
    ],
    "b3_v02.ass": [
        (0.0, 5.0, "Eu comecei muito por confianca e indicacao."),
        (5.0, 10.0, "Agora minha meta e clientes por trafego pago."),
        (10.0, 18.0, "Meus resultados com trafego pago estao muito bons."),
        (18.0, 26.0, "Fiz uma campanha para uma maquina de ate R$50 mil."),
        (26.0, 33.0, "Consegui vender gastando apenas R$100 em anuncios!")
    ],
    "b3_v03.ass": [
        (0.0, 5.0, "Hoje eu mando um audio para o agente executar a tarefa."),
        (5.0, 10.0, "E muito mais facil falar por audio."),
        (10.0, 18.0, "Quando vejo uma oportunidade na rua, faco na hora."),
        (18.0, 28.0, "Se for algo mais longo, salvo a nota de voz no celular."),
        (28.0, 36.0, "Depois eu transcrevo e organizo tudo no computador."),
        (36.0, 43.0, "O segredo e nao perder a ideia enquanto ela surge!")
    ],
    "b3_v04.ass": [
        (0.0, 6.0, "Fala uma profissao para a gente testar nessa API."),
        (6.0, 12.0, "Vamos testar Tecnico de Seguranca."),
        (12.0, 20.0, "Nem vou colocar acento para ver a interpretacao."),
        (20.0, 30.0, "Ela esta explicando o que o profissional faz!"),
        (30.0, 42.0, "Eu nao quero a descricao, quero encontrar as vagas."),
        (42.0, 55.0, "Na segunda tentativa vieram alguns resultados."),
        (55.0, 68.0, "Mas varios estavam mal formatados ou com links quebrados."),
        (68.0, 80.0, "Minha nota foi 4/10. Teste antes de usar no seu projeto.")
    ],
    "b3_v05.ass": [
        (0.0, 8.0, "Voce envia uma URL e ela devolve metadados e cores."),
        (8.0, 18.0, "Essa API automatiza acoes no navegador e faz captura."),
        (18.0, 28.0, "Gera PDF, obtem paleta de cores e identifica tecnologias."),
        (28.0, 40.0, "Util para monitorar paginas, criar previews e extrair dados!")
    ],
    "b3_v06.ass": [
        (0.0, 8.0, "Dados de mais de 200 paises sem criar sua base."),
        (8.0, 18.0, "A API do Banco Mundial fornece dados economicos e sociais."),
        (18.0, 32.0, "Estou em um projeto e quero entender os mercados das empresas."),
        (32.0, 44.0, "Ela traz todo o contexto economico macro do pais."),
        (44.0, 56.0, "Excelente para entender o mercado ao redor da empresa!")
    ],
    "b3_r01.ass": [
        (0.0, 6.0, "Esta falando que nao posso mexer porque a camera esta indisponivel."),
        (6.0, 12.0, "So que eu tambem nao consigo excluir a camera!"),
        (12.0, 18.0, "Nao foi possivel excluir, mas tambem nao posso usar."),
        (18.0, 24.0, "Qual e o sentido desse erro do TikTok? 😂")
    ]
}

for filename, events in subs_data.items():
    filepath = os.path.join(subs_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER)
        for start, end, text in events:
            f.write(f"Dialogue: 0,{format_time(start)},{format_time(end)},Default,,0,0,0,,{text}\n")
    print(f"✅ Criado ASS: {filename}")

print("Legendas ASS do Bloco 3 geradas!")
