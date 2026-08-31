# 🎬 Análise de Lives e Postagem Automática

Pipeline automatizado em Python/FFmpeg para transcrição, edição cinemática vertical (Reels/TikTok) e agendamento de postagens via WoopSocial API.

---

## 📌 Funcionalidades Principais

- **Transcrição Literal com Timestamps**: Geração de transcrição completa via Whisper AI a partir de gravações de lives longas (ex: 3 horas).
- **Corte & Edição Cinemática (FFmpeg)**:
  - Formato vertical 9:16 (`crop=ih*9/16:ih...`).
  - **Focus Zoom Multi-Câmera**: Alternância dinâmica de enquadramento (100% → 108%).
  - **Títulos Stylized**: Cartão dark elegante posicionado na altura do enquadramento superior da câmera (`y=440`) com borda sutil.
  - **Legendas Kinéticas (ASS)**: Burn-in de legendas em tempo real extraídas da fala verdadeira do Whisper.
  - **Full Screen Fix**: Ajuste de proporção para trechos de gravação de tela / sem câmera.
- **Histórias Narrativas (Storytelling ARCO)**: Concatenação de trechos não-contíguos da live criando narrativas envolventes (*Hook → Story → Shift*).
- **Agendamento Automático (WoopSocial API)**:
  - Upload de vídeos em partes (chunked upload).
  - Distribuição e agendamento de posts no TikTok (`@kthyeu`).
  - Gerenciamento inteligente de limite de storage de 1 GB com remoção de mídias órfãs.

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

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- FFmpeg instalado no PATH
- Chave de API do WoopSocial

### 1. Renderizar Histórias Narrativas
```bash
python "Scripts e Transcrições/render_5_stories_real_subs.py"
```

### 2. Agendar Postagens
```bash
python "Scripts e Transcrições/redistribute_5_stories_wed_to_sun.py"
```

---

*Desenvolvido para automação e escala de criação de conteúdo.*
