# app.py

import streamlit as st
import re
from typing import Optional, Dict, Any, List

# --- Mapeamentos Unicode para Estilos ---
_BOLD_MAP = {
    'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆', 'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍', 'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔', 'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
    'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠', 'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
    '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗',
}

_ITALIC_MAP = {
    'A': '𝘈', 'B': '𝘉', 'C': '𝘊', 'D': '𝘋', 'E': '𝘌', 'F': '𝘍', 'G': '𝘎', 'H': '𝘏', 'I': '𝘐', 'J': '𝘑', 'K': '𝘒', 'L': '𝘓', 'M': '𝘔', 'N': '𝘕', 'O': '𝘖', 'P': '𝘗', 'Q': '𝘘', 'R': '𝘙', 'S': '𝘚', 'T': '𝘛', 'U': '𝘜', 'V': '𝘝', 'W': '𝘞', 'X': '𝘟', 'Y': '𝘠', 'Z': '𝘡',
    'a': '𝘢', 'b': '𝘣', 'c': '𝘤', 'd': '𝘥', 'e': '𝘦', 'f': '𝘧', 'g': '𝘨', 'h': '𝘩', 'i': '𝘪', 'j': '𝘫', 'k': '𝘬', 'l': '𝘭', 'm': '𝘮', 'n': '𝘯', 'o': '𝘰', 'p': '𝘱', 'q': '𝘲', 'r': '𝘳', 's': '𝘴', 't': '𝘵', 'u': '𝘶', 'v': '𝘷', 'w': '𝘸', 'x': '𝘹', 'y': '𝘺', 'z': '𝘻',
}

_MONOSPACE_MAP = {
    'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶', 'H': '𝙷', 'I': '𝙸', 'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽', 'O': '𝙾', 'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄', 'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚺',
    'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏', 'g': '𝚐', 'h': '𝚑', 'i': '𝚒', 'j': '𝚓', 'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗', 'o': '𝚘', 'p': '𝚙', 'q': '𝚚', 'r': '𝚛', 's': '𝚜', 't': '𝚝', 'u': '𝚞', 'v': '𝚟', 'w': '𝚠', 'x': '𝚡', 'y': '𝚢', 'z': '𝚣',
    '0': '𝟶', '1': '𝟷', '2': '𝟸', '3': '𝟹', '4': '𝟺', '5': '𝟻', '6': '𝟼', '7': '𝟽', '8': '𝟾', '9': '𝟿',
}

_STRIKETHROUGH_CHAR = '\u0336' # Combining Long Stroke Overlay

# --- Funções Auxiliares para Aplicar Estilos ---
def _apply_mapping(text: str, mapping: Dict[str, str]) -> str:
    """Aplica um mapeamento de caracteres a uma string."""
    return "".join(mapping.get(char, char) for char in text)

def _to_bold(text: str) -> str:
    """Converte texto para Unicode Bold."""
    return _apply_mapping(text, _BOLD_MAP)

def _to_italic(text: str) -> str:
    """Converte texto para Unicode Italic."""
    return _apply_mapping(text, _ITALIC_MAP)

def _to_monospace(text: str) -> str:
    """Converte texto para Unicode Monospace."""
    return _apply_mapping(text, _MONOSPACE_MAP)

def _to_strikethrough(text: str) -> str:
    """Aplica o caractere de Strikethrough a cada caractere."""
    # Aplica a cada char que não seja um caractere de combinação já existente
    return "".join(char + _STRIKETHROUGH_CHAR if '\u0300' <= char <= '\u036f' else char + _STRIKETHROUGH_CHAR for char in text)


# --- Funções de Substituição para Regex ---
def _code_replacer(match: re.Match) -> str:
    """Substitui `code` por texto monospace."""
    return _to_monospace(match.group(1))

def _strikethrough_replacer(match: re.Match) -> str:
    """Substitui ~~strikethrough~~ por texto riscado."""
    return _to_strikethrough(match.group(1))

def _bold_replacer_star(match: re.Match) -> str:
    """Substitui **bold** por texto bold Unicode."""
    return _to_bold(match.group(1))

def _bold_replacer_underscore(match: re.Match) -> str:
    """Substitui __bold__ por texto bold Unicode."""
    return _to_bold(match.group(1))

def _italic_replacer_star(match: re.Match) -> str:
    """Substitui *italic* por texto italic Unicode."""
    return _to_italic(match.group(1))

def _italic_replacer_underscore(match: re.Match) -> str:
    """Substitui _italic_ por texto italic Unicode."""
    return _to_italic(match.group(1))

def _link_replacer(match: re.Match) -> str:
    """Substitui [text](url) por text."""
    return match.group(1)

# --- Função Principal ---
def markdown_to_unicode(markdown_text: str, options: Optional[Dict[str, Any]] = None) -> str:
    """
    Converte uma string Markdown básica para uma string usando caracteres Unicode estilizados.

    Args:
        markdown_text: A string contendo Markdown.
        options: Um dicionário opcional para configurar a conversão.
                 Opções suportadas:
                 - 'list_bullet' (str): O caractere a usar para itens de lista não ordenada (padrão: '•').
                 - 'header_style' (str): Estilo para cabeçalhos ('strip' para remover #, 'bold' para aplicar bold, padrão: 'strip').
                 - 'horizontal_rule_char' (str): O caractere a usar para a linha horizontal (padrão: '─').
                 - 'horizontal_rule_length' (int): O comprimento da linha horizontal (padrão: 20).


    Returns:
        A string convertida com caracteres Unicode.
    """
    if not isinstance(markdown_text, str):
        return "" # Em um app web, retornar vazio ou erro amigável é melhor.

    # 1. Configurar Opções
    effective_options: Dict[str, Any] = {
        'list_bullet': '•',
        'header_style': 'strip', # 'strip' ou 'bold'
        'horizontal_rule_char': '─', # Caractere para HR
        'horizontal_rule_length': 20, # Comprimento padrão da HR
    }
    if options:
        # Validação básica para garantir que as opções passadas são válidas
        # e não causam erros (como length=0 ou char vazio)
        for key, value in options.items():
            if key in effective_options:
                 if key == 'list_bullet' and isinstance(value, str) and value != "":
                      effective_options[key] = value
                 if key == 'header_style' and value in ['strip', 'bold']:
                      effective_options[key] = value
                 if key == 'horizontal_rule_char' and isinstance(value, str) and value != "":
                     effective_options[key] = value[0] # Pega apenas o primeiro caractere
                 if key == 'horizontal_rule_length' and isinstance(value, int) and value > 0:
                      effective_options[key] = value


    list_bullet = effective_options['list_bullet']
    header_style = effective_options['header_style']
    hr_char = effective_options['horizontal_rule_char']
    hr_length = effective_options['horizontal_rule_length']

    processed_lines: List[str] = []

    # 2. Processar elementos de nível de bloco (linha por linha)
    lines = markdown_text.splitlines()

    for line in lines:
        # Ignorar linhas vazias no processamento de bloco
        if not line.strip():
            processed_lines.append("") # Mantém a quebra de linha original
            continue

        # Horizontal Rule (deve ser verificado primeiro, pois consome a linha inteira)
        # Regex para HR: 3 ou mais -, *, ou _ com espaços opcionais ao redor, na linha inteira
        if re.fullmatch(r'\s*([-*_])(\s*\1){2,}\s*', line):
             processed_lines.append(hr_char * hr_length)
             continue # Pula para a próxima linha

        # Blockquote
        # Regex para Blockquote: Linha começando com > e espaço opcional
        blockquote_match = re.match(r'^\s*>\s*(.*)$', line)
        if blockquote_match:
            processed_lines.append(f"| {blockquote_match.group(1)}")
            continue # Pula para a próxima linha

        # Unordered List
        # Regex para Lista Não Ordenada: Linha começando com *, -, ou + e DEVE ter um ou mais espaços depois
        # ALTERAÇÃO AQUI: De '\s*' para '\\s+' para exigir espaço(s) após o marcador
        list_match = re.match(r'^\s*[-*+]\\s+(.*)$', line)
        if list_match:
            processed_lines.append(f"{list_bullet} {list_match.group(1)}")
            continue # Pula para a próxima linha

        # Headers
        # Regex para Headers: Linha começando com 1 ou mais # e espaço
        header_match = re.match(r'^(#+)\s*(.*)$', line)
        if header_match:
            header_text = header_match.group(2)
            if header_style == 'bold':
                processed_lines.append(_to_bold(header_text))
            else: # Default 'strip'
                processed_lines.append(header_text)
            continue # Pula para a próxima linha

        # Se não for um elemento de bloco conhecido, adicione a linha como está
        processed_lines.append(line)

    # Junta as linhas processadas para processar elementos inline
    intermediate_text = "\n".join(processed_lines)

    # 3. Processar elementos Inline
    result_text = intermediate_text

    # Ordem de processamento inline pode importar.
    # Começando com elementos mais "internos" ou com caracteres especiais.

    # Código Inline: `code` -> monospace
    result_text = re.sub(r'(?<!\\)`(.+?)(?<!\\)`', _code_replacer, result_text)

    # Strikethrough: ~~strikethrough~~ -> riscado
    result_text = re.sub(r'~~(.+?)~~', _strikethrough_replacer, result_text)

    # Bold: **bold** ou __bold__ -> bold Unicode
    # Processa **
    result_text = re.sub(r'(?<!\*)\*\*(.+?)\*\*(?!\*)', _bold_replacer_star, result_text)
    # Processa __
    result_text = re.sub(r'(?<!_)__(.+?)__(?!_)', _bold_replacer_underscore, result_text)

    # Italic: *italic* ou _italic_ -> italic Unicode
    # Cuidado: Evitar * em **texto**, _ em __texto__
    result_text = re.sub(r'(?<![\\*])\*([^*]+?)\*(?![\\*])', _italic_replacer_star, result_text)
    result_text = re.sub(r'(?<![\\_])_([^_]+?)_(?![\\_])', _italic_replacer_underscore, result_text)

    # Link: [text](url) -> text
    result_text = re.sub(r'\[(.+?)\]\(.+?\)', _link_replacer, result_text)

    # Retornar o texto final com as conversões
    return result_text


# --- Interface Streamlit ---

st.set_page_config(page_title="Markdown to Unicode Converter", layout="wide")

st.title("✏️ Markdown to Unicode Converter")

st.write("""
Use esta ferramenta para converter texto formatado com Markdown básico
(bold, italic, code, strikethrough, links, cabeçalhos, listas, blockquotes, linhas horizontais)
em texto usando caracteres Unicode estilizados que podem ser usados em redes sociais, etc.
""")

# Área de Input
markdown_input = st.text_area(
    "Cole seu texto Markdown aqui:",
    value="""# Histórico da Conversa - Guia de Linha Amarela e Pavimentação

**Tópico:** Visão Geral
**Data:** 2025-06-07 10:25:08

---

**User:**
pode explicar e dar exemplo sobre a postagem e em que tipo de trabalho se utiliza?

---
**Assistant:**
Entendido. Com base na postagem e na natureza das barras de FRP como armadura para concreto, posso explicar em que tipos de obras de engenharia civil esse material é utilizado, especialmente sob a luz de normas como a ABNT NBR 17196:2025 que regulamentam seu uso em estruturas de concreto armado.

1.  **Ambientes Agressivos e com Alto Risco de Corrosão:** Este é o principal benefício das barras de FRP. Diferentemente do aço, elas não sofrem corrosão quando expostas à umidade, cloretos (sal) ou sulfatos. Portanto, são ideais para:
    *   Estruturas Costeiras e Marinhas: Muros de contenção, píeres, tabuleiros de pontes sobre água salgada, estruturas em portos.
    *   Estruturas Rodoviárias e Aeroportuárias: Tabuleiros de pontes e viadutos, barreiras de concreto (guard-rails), pisos de estacionamentos em regiões onde se utiliza sal para degelo (agente corrosivo para o aço).

2.  **Aplicações Não Magnéticas e Eletricamente Não Condutivas:** As barras de FRP não são magnéticas nem condutoras de eletricidade, o que as torna essenciais em:
    *   Hospitais: Salas de ressonância magnética (MRI), onde campos magnéticos devem ser isolados.
    *   Subestações Elétricas: Onde a interferência eletromagnética precisa ser minimizada.
    *   Estruturas para Equipamentos Eletrônicos Sensíveis: Laboratórios, centros de dados.
    *   Áreas de Pesquisa: Onde são realizados experimentos que envolvem campos magnéticos ou corrente elétrica.

3.  **Obras de Tunelamento:** Especialmente em segmentação de túneis ou estruturas temporárias, barras de FRP podem ser usadas pois são mais fáceis de serem cortadas por tuneladoras (TBMs) caso fiquem no caminho, sendo menos abrasivas para os equipamentos do que o aço.

4.  **Peso Reduzido:** Embora não seja o fator principal na maioria das aplicações estruturais em concreto, as barras de FRP são significativamente mais leves que as barras de aço, o que pode ser uma vantagem logística no transporte e manuseio em canteiro.



Em resumo, as barras de FRP são utilizadas em obras de engenharia civil onde a durabilidade em ambientes corrosivos ou a necessidade de não-magneticidade e não-condutividade elétrica são requisitos críticos.

---
---- Guia de Linha Amarela e Pavimentação ----
Desenvolvido com ❤️ por Engº Paulo R. V. Silva!
Este assistente utiliza IA Generativa.
https://lnkd.in/d-6hnqGs
""", # Use o seu texto de teste como valor padrão
    height=500
)

# Opções na Sidebar
st.sidebar.header("Opções de Conversão")

list_bullet_char = st.sidebar.text_input(
    "Caractere para Lista Não Ordenada:",
    value="•",
    max_chars=1 # Geralmente, bullets são um único caractere
)

header_style_option = st.sidebar.selectbox(
    "Estilo dos Cabeçalhos:",
    options=['strip', 'bold'], # strip = remove #, bold = aplica estilo bold
    index=0 # strip como padrão
)

hr_char_option = st.sidebar.text_input(
    "Caractere para Linha Horizontal:",
    value="─", # U+2500 BOX DRAWINGS LIGHT HORIZONTAL
    max_chars=1 # Geralmente, HR usa um único caractere
)

hr_length_option = st.sidebar.number_input(
    "Comprimento da Linha Horizontal:",
    min_value=5,
    max_value=100,
    value=30,
    step=5
)


# Coleta as opções em um dicionário
options_dict = {
    'list_bullet': list_bullet_char,
    'header_style': header_style_option,
    'horizontal_rule_char': hr_char_option,
    'horizontal_rule_length': hr_length_option,
}

# Realiza a conversão
if markdown_input:
    unicode_output = markdown_to_unicode(markdown_input, options_dict)

    # Área de Output
    st.subheader("Texto Unicode Convertido:")

    # Use st.text para exibir o texto bruto com os caracteres unicode
    # Isso evita que Streamlit tente interpretar o Markdown na saída,
    # mostrando exatamente a string unicode resultante.
    st.text(unicode_output)

    st.markdown("""
    <small>Copie o texto acima. A aparência pode variar dependendo da fonte e plataforma onde ele for colado.</small>
    """, unsafe_allow_html=True)
else:
     st.info("Cole seu texto Markdown na caixa acima para ver a conversão.")

st.markdown("---")
st.write("Desenvolvido por sua IA assistente, baseado no trabalho de cstayyab.")
st.markdown("""
**Markdown Básico Suportado:**
*   `**bold**` ou `__bold__` -> Negrito Unicode (𝐀)
*   `*italic*` ou `_italic_` -> Itálico Unicode (𝘈)
*   ``` `code` ``` -> Monospace Unicode (𝚊)
*   ``` ~~strikethrough~~ ``` -> Riscado (T̶e̶x̶t̶)
*   ``` [text](url) ``` -> Apenas o texto do link
*   ``` # Header ```, ``` ## Subheader ```, etc. -> Texto simples ou Negrito (configurável)
*   ``` > Blockquote ``` -> Texto precedido por `|`
*   ``` * Item ```, ``` - Item ```, ``` + Item ``` **(seguido por espaço)** -> Texto precedido por marcador de lista (configurável)
*   ``` --- ```, ``` *** ```, ``` ___ ``` **(em uma linha isolada)** -> Linha horizontal (configurável)
""")