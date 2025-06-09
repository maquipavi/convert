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
    return "".join(char + _STRIKETHROUGH_CHAR for char in text)

# --- Funções de Substituição para Regex ---
def _code_replacer(match: re.Match) -> str:
    """Substitui `code` por texto monospace."""
    return _to_monospace(match.group(1))

def _strikethrough_replacer(match: re.Match) -> str:
    """Substitui ~~strikethrough~~ por texto riscado."""
    return _to_strikethrough(match.group(1))

def _bold_replacer(match: re.Match) -> str:
    """Substitui **bold** ou __bold__ por texto bold Unicode."""
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
                 - 'horizontal_rule_char' (str): O caractere a usar para a linha horizontal (padrão: '─').
                 - 'horizontal_rule_length' (int): O comprimento da linha horizontal (padrão: 20).

    Returns:
        A string convertida com caracteres Unicode.
    """
    if not isinstance(markdown_text, str):
        raise TypeError("Input must be a string.")

    # 1. Configurar Opções
    effective_options: Dict[str, Any] = {
        'horizontal_rule_char': '─',  # Caractere para HR
        'horizontal_rule_length': 20,  # Comprimento padrão da HR
    }

    if options:
        for key, value in options.items():
            if key in effective_options:
                if key == 'horizontal_rule_char' and not isinstance(value, str):
                    continue
                if key == 'horizontal_rule_length' and not isinstance(value, int):
                    continue
                effective_options[key] = value

    hr_char = effective_options['horizontal_rule_char']
    hr_length = effective_options['horizontal_rule_length']

    processed_lines: List[str] = []

    # 2. Processar elementos de nível de bloco (linha por linha)
    lines = markdown_text.splitlines()

    for line in lines:
        # Horizontal Rule (deve ser verificado primeiro, pois consome a linha inteira)
        if re.fullmatch(r'\s*([-*_])(\s*\1){2,}\s*', line):
            processed_lines.append(hr_char * hr_length)
            continue

        # Blockquote
        blockquote_match = re.match(r'^\s*>\s*(.*)$', line)
        if blockquote_match:
            processed_lines.append(f"| {blockquote_match.group(1)}")
            continue

        # Unordered List
        list_match = re.match(r'^\s*[-*+]\s*(.*)$', line)
        if list_match:
            # Garante que o texto da lista não seja interpretado como Markdown (ex: bold)
            list_text = list_match.group(1)
            processed_lines.append(f"• {list_text}")
            continue

        # Headers
        header_match = re.match(r'^(#+)\s*(.*)$', line)
        if header_match:
            header_text = header_match.group(2)
            processed_lines.append(header_text)
            continue

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
    # Processa ** e __ com a mesma função
    result_text = re.sub(r'(?<![\*\_])(\*\*|__)(.+?)(\*\*|__)(?![\*\_])', _bold_replacer, result_text)

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
    value="""# Exemplo de Markdown
## Título
Olá, **mundo**! Este é um *exemplo* de texto.

Podemos usar `código inline` e ~~texto riscado~~.
Aqui está um [link para o Google](https://google.com).

> Isto é um bloco de citação.
> Outra linha da citação.

Lista de compras:
* Maçãs
- Bananas
+ Cerejas

---

Uma linha horizontal.

Mais texto.
***

Fim do exemplo.
""",
    height=300
)

# Opções na Sidebar
st.sidebar.header("Opções de Conversão")

hr_char_option = st.sidebar.text_input(
    "Caractere para Linha Horizontal:",
    value="─"  # U+2500 BOX DRAWINGS LIGHT HORIZONTAL
)

hr_length_option = st.sidebar.number_input(
    "Comprimento da Linha Horizontal:",
    min_value=5,
    max_value=100,
    value=30,
    step=1
)

# Coleta as opções em um dicionário
options_dict = {
    'horizontal_rule_char': hr_char_option,
    'horizontal_rule_length': hr_length_option,
}

# Realiza a conversão
if markdown_input:
    unicode_output = markdown_to_unicode(markdown_input, options_dict)

    # Área de Output
    st.subheader("Texto Unicode Convertido:")

    st.text(unicode_output)  # Use st.text para exibir o texto bruto com os caracteres unicode

    st.markdown("""
    <small>Copie o texto acima. A aparência pode variar dependendo da fonte e plataforma onde ele for colado.</small>
    """, unsafe_allow_html=True)
else:
    st.info("Cole seu texto Markdown na caixa acima para ver a conversão.")

st.markdown("---")
st.write("Desenvolvido com ❤️ por Engº Paulo Rogério Veiga Silva!")
st.markdown("""
**Markdown Básico Suportado:**
*   `**bold**` ou `__bold__` -> Negrito Unicode (𝐀)
*   `*italic*` ou `_italic_` -> Itálico Unicode (𝘈)
*   ``` `code` ``` -> Monospace Unicode (𝚊)
*   ``` ~~strikethrough~~ ``` -> Riscado (T̶e̶x̶t̶)
*   ``` [text](url) ``` -> Apenas o texto do link
*   ``` # Header ```, ``` ## Subheader ```, etc. -> Texto simples ou Negrito (configurável)
*   ``` > Blockquote ``` -> Texto precedido por `|`
*   ``` * Item ```, ``` - Item ```, ``` + Item ``` -> Texto precedido por marcador de lista (configurável)
*   ``` --- ```, ``` *** ```, ``` ___ ``` -> Linha horizontal (configurável)
""")
