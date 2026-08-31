# 🎬 Análise de Lives e Postagem Automática

Sistema automatizado em Python, Whisper AI e FFmpeg para análise de lives longas, extração de cortes de alto impacto (Hooks, Stories, Shifts), edição cinemática vertical (Reels/TikTok) e agendamento automático de postagens via WoopSocial API.

---

## 💡 Como o Sistema Funciona por Dentro (Arquitetura & Critérios)

### 🧠 1. Critérios de Qualidade & Escolha dos Cortes

A seleção dos trechos é realizada via **Whisper AI + Análise de Linguagem e Estruturação Narrativa**, buscando 3 elementos essenciais em cada vídeo:

1. 🪝 **O Gancho (Hook - Primeiros 3 a 5 segundos)**:
   - Procura por declarações fortes, frases de impacto ou perguntas diretas (ex: *"Eu comecei vendendo perfume por R$70 por dia"*, *"Não coloque o código da sua empresa no ChatGPT"*).
   - Elimina pausas iniciais, vícios de linguagem ("éee...", hesitações) para iniciar imediatamente na frase de maior retenção.

2. 📖 **O Desenvolvimento (Body/Story - 30 a 60 segundos)**:
   - Identifica momentos em que há a explicação de uma **solução prática, um erro cometido ou uma história pessoal de superação**.
   - Filtra e ignora interações aleatórias com o chat da live, silêncios, pausas para água ou ajustes técnicos.

3. 💡 **O Fechamento / Aprendizado (Close/Shift - Últimos 5 segundos)**:
   - Busca uma conclusão com moral da história, sacada prática ou frase de efeito (ex: *"Gratuito não é barato quando custa horas de teste"*).

---

### 🎭 2. Concatenação de Histórias Narrativas (Multi-Atos)

Diferente de sistemas tradicionais que apenas recortam blocos contínuos de 1 minuto, este sistema realiza **Concatenação Inteligente de Trechos Não-Contíguos**:

- Identifica momentos relacionados espalhados em timestamps distantes da live (ex: min `1:05:45` e min `1:12:23`).
- Junta os trechos em um único vídeo fluido de ~80 segundos, construindo uma história completa de início, meio e fim sem perder a atenção do espectador.

---

### 🎨 3. Pipeline de Edição Cinemática (FFmpeg)

O script de renderização aplica as seguintes transformações automatizadas:

1. **Enquadramento Vertical (9:16)**: Recorte vertical centralizado na webcam do palestrante (`crop=ih*9/16:ih...`).
2. **Focus Zoom (Corte Multi-Câmera)**: Alternância dinâmica de escala (100% → 108%) nas transições de assunto ou ênfases emocionais, simulando troca de câmeras.
3. **Título Estilizado na Altura da Câmera (`y=440`)**:
   - Mede o enquadramento do rosto e desenha um cartão dark com linha superior amarela **ajustado exatamente no limite superior da webcam**, sem cobrir a pessoa.
4. **Legendas Kinéticas (ASS)**:
   - Alinhadas palavra por palavra com o tempo preciso gerado pelo Whisper AI.
   - Renderizadas em amarelo/branco centralizadas na tela com realce conforme a fala.
5. **Full Screen Fix (Ajustes de Tela)**:
   - Para trechos de compartilhamento de tela ou slides sem câmera, aplica zoom e preenchimento total 9:16.
6. **Normalização de Áudio (Loudnorm)**: Volume ajustado para **-16 LUFS** (padrão de redes sociais).

---

### 🚀 4. Agendamento Automático no TikTok (WoopSocial API)

1. **Upload em Partes (Chunked Upload)**: Divisão dos vídeos em partes pequenas com requisições seguras para a API da WoopSocial.
2. **Gestão Inteligente de Storage**: Monitoramento do limite de 1 GB do servidor e remoção automática de arquivos de mídia órfãos.
3. **Gerador de Captions & Hashtags**: Montagem de textos nativos com emojis e hashtags otimizadas (`#Empreendedorismo #Programacao #TrafegoPago`).
4. **Distribuição no Cronograma**: Agendamento espaçado nos horários de pico (09h, 12h, 15h, 18h, 22h BRT), cobrindo a grade diária até o final de semana.

---

## 📂 Estrutura do Repositório

```text
├── Histórias Narrativas (5 Vídeos + RAW)/   # Os 5 cortes narrativos mestre + versão RAW sem edição
├── Cortes Bloco 3/                          # Cortes analisados por minutagem (1:04:30 - 1:30:19)
├── Cortes Bloco 2/                          # Cortes human-crafted do bloco 2
├── Cortes Bloco 1/                          # Cortes do bloco 1 (15 vídeos)
└── Scripts e Transcrições/                  # Transcrição .md completa (3h) e scripts Python de renderização e agendamento
```

---

## 💻 Como Executar

### Pré-requisitos
- Python 3.10+
- FFmpeg instalado e no PATH do sistema
- Credenciais da API WoopSocial

### 1. Executar Renderização das Histórias Narrativas
```bash
python "Scripts e Transcrições/render_5_stories_real_subs.py"
```

### 2. Executar Agendamento Automático
```bash
python "Scripts e Transcrições/redistribute_5_stories_wed_to_sun.py"
```

---

*Desenvolvido para automação, escala e retenção em redes sociais.*
