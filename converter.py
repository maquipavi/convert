# -*- coding: utf-8 -*-
"""Converte texto Markdown selecionado para caracteres Unicode."""

import re
from typing import Dict, Callable, Optional

# --- Mapeamentos de Caracteres Unicode ---

# Negrito (Sans-Serif Bold)
UNICODE_BOLD: Dict[str, str] = {
    'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚',
    'H': '𝗛', 'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡',
    'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨',
    'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭',
    'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴',
    'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻',
    'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂',
    'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
    '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲',
    '7': '𝟳', '8': '𝟴', '9': '𝟵'
}

# Itálico (Sans-Serif Italic)
UNICODE_ITALIC: Dict[str, str] = {
    'A': '𝘈', 'B': '𝘉', 'C': '𝘊', 'D': '𝘋', 'E': '𝘌', 'F': '𝘍', 'G': '𝘎',
    'H': '𝘏', 'I': '𝘐', 'J': '𝘑', 'K': '𝘒', 'L': '𝘓', 'M': '𝘔', 'N': '𝘕',
    'O': '𝘖', 'P': '𝘗', 'Q': '𝘘', 'R': '𝘙', 'S': '𝘚', 'T': '𝘛', 'U': '𝘜',
    'V': '𝘝', 'W': '𝘞', 'X': '𝘟', 'Y': '𝘠', 'Z': '𝘡',
    'a': '𝘢', 'b': '𝘣', 'c': '𝘤', 'd': '𝘥', 'e': '𝘦', 'f': '𝘧', 'g': '𝘨',
    'h': '𝘩', 'i': '𝘪', 'j': '𝘫', 'k': '𝘬', 'l': '𝘭', 'm': '𝘮', 'n': '𝘯',
    'o': '𝘰', 'p': '𝘱', 'q': '𝘲', 'r': '𝘳', 's': '𝘴', 't': '𝘵', 'u': '𝘶',
    'v': '𝘷', 'w': '𝘸', 'x': '𝘹', 'y': '𝘺', 'z': '𝘻'
}

# Negrito-Itálico (Sans-Serif Bold Italic)
UNICODE_BOLD_ITALIC: Dict[str, str] = {
    'A': '𝘼', 'B': '𝘽', 'C': '𝘾', 'D': '𝘿', 'E': '𝙀', 'F': '𝙁', 'G': '𝙂',
    'H': '𝙃', 'I': '𝙄', 'J': '𝙅', 'K': '𝙆', 'L': '𝙇', 'M': '𝙈', 'N': '𝙉',
    'O': '𝙊', 'P': '𝙋', 'Q': '𝙌', 'R': '𝙍', 'S': '𝙎', 'T': '𝙏', 'U': '𝙐',
    'V': '𝙑', 'W': '𝙒', 'X': '𝙓', 'Y': '𝙔', 'Z': '𝙕',
    'a': '𝙖', 'b': '𝙗', 'c': '𝙘', 'd': '𝙙', 'e': '𝙚', 'f': '𝙛', 'g': '𝙜',
    'h': '𝙝', 'i': '𝙞', 'j': '𝙟', 'k': '𝙠', 'l': '𝙡', 'm': '𝙢', 'n': '𝙣',
    'o': '𝙤', 'p': '𝙥', 'q': '𝙦', 'r': '𝙧', 's': '𝙨', 't': '𝙩', 'u': '𝙪',
    'v': '𝙫', 'w': '𝙬', 'x': '𝙭', 'y': '𝙮', 'z': '𝙯'
}

# Script (Caligráfico)
UNICODE_SCRIPT: Dict[str, str] = {
    'A': '𝒜', 'B': 'ℬ', 'C': '𝒞', 'D': '𝒟', 'E': 'ℰ', 'F': 'ℱ', 'G': '𝒢',
    'H': 'ℋ', 'I': 'ℐ', 'J': '𝒥', 'K': '𝒦', 'L': 'ℒ', 'M': 'ℳ', 'N': '𝒩',
    'O': '𝒪', 'P': '𝒫', 'Q': '𝒬', 'R': 'ℛ', 'S': '𝒮', 'T': '𝒯', 'U': '𝒰',
    'V': '𝒱', 'W': '𝒲', 'X': '𝒳', 'Y': '𝒴', 'Z': '𝒵',
    'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': 'ℯ', 'f': '𝒻', 'g': 'ℊ',
    'h': '𝒽', 'i': '𝒾', 'j': '𝒿', 'k': '𝓀', 'l': '𝓁', 'm': '𝓂', 'n': '𝓃',
    'o': 'ℴ', 'p': '𝓅', 'q': '𝓆', 'r': '𝓇', 's': '𝓈', 't': '𝓉', 'u': '𝓊',
    'v': '𝓋', 'w': '𝓌', 'x': '𝓍', 'y': '𝓎', 'z': '𝓏'
}

# Script Bold (Caligráfico Negrito)
UNICODE_SCRIPT_BOLD: Dict[str, str] = {
    'A': '𝓐', 'B': '𝓑', 'C': '𝓒', 'D': '𝓓', 'E': '𝓔', 'F': '𝓕', 'G': '𝓖',
    'H': '𝓗', 'I': '𝓘', 'J': '𝓙', 'K': '𝓚', 'L': '𝓛', 'M': '𝓜', 'N': '𝓝',
    'O': '𝓞', 'P': '𝓟', 'Q': '𝓠', 'R': '𝓡', 'S': '𝓢', 'T': '𝓣', 'U': '𝓤',
    'V': '𝓥', 'W': '𝓦', 'X': '𝓧', 'Y': '𝓨', 'Z': '𝓩',
    'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰',
    'h': '𝓱', 'i': '𝓲', 'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷',
    'o': '𝓸', 'p': '𝓹', 'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽', 'u': '𝓾',
    'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃'
}

# --- Funções Auxiliares de Conversão de Caracteres ---

def _convert_char(char: str, mapping: Dict[str, str]) -> str:
    """Converte um único caractere usando o mapeamento fornecido."""
    return mapping.get(char, char)

def _convert_text(text: str, mapping: Dict[str, str]) -> str:
    """Converte uma string inteira usando o mapeamento fornecido."""
    converted_chars = [_convert_char(char, mapping) for char in text]
    # Verifica se alguma conversão realmente ocorreu
    if all(original == converted for original, converted in zip(text, converted_chars)):
        return text # Retorna o texto original se nada mudou
    return ''.join(converted_chars)

def _convert_strikethrough(text: str) -> str:
    """Adiciona o caractere combinante de tachado a cada caractere da string."""
    processed_text = ""
    for char in text:
        if 0x1D400 <= ord(char) <= 0x1D7FF:
            processed_text += char
        else:
            processed_text += char + '\u0336'
    return processed_text

# --- Funções de Conversão de Markdown ---

def convert_bold(text: str, options: Optional[Dict] = None) -> str:
    """Converte Markdown bold (`**text**` ou `__text__`) para Unicode."""
    style = options.get('bold_style', 'sans') if options else 'sans'
    mapping = UNICODE_BOLD
    if style == 'script':
        mapping = UNICODE_SCRIPT_BOLD

    def replace_bold(match: re.Match) -> str:
        content = match.group(2)
        if not content or content.isspace():
            return match.group(0)
        converted_content = _convert_text(content, mapping)
        # Se a conversão não alterou o conteúdo (ex: números sem mapeamento), retorna o original com marcadores
        if converted_content == content:
            return match.group(0)
        return converted_content

    bold_regex = r'(\*\*|__)(.+?)\1'
    return re.sub(bold_regex, replace_bold, text)

def convert_italic(text: str, options: Optional[Dict] = None) -> str:
    """Converte Markdown italic (`*text*` ou `_text_`) para Unicode."""
    style = options.get('italic_style', 'sans') if options else 'sans'
    mapping = UNICODE_ITALIC
    if style == 'script':
        mapping = UNICODE_SCRIPT

    def replace_italic(match: re.Match) -> str:
        content = match.group(2)
        if not content or content.isspace():
            return match.group(0)
        converted_content = _convert_text(content, mapping)
        # Se a conversão não alterou o conteúdo, retorna o original com marcadores
        if converted_content == content:
            return match.group(0)
        return converted_content

    italic_regex_with_content = r'(\*|_)(.+?)\1'
    return re.sub(italic_regex_with_content, replace_italic, text)

def convert_bold_italic(text: str, options: Optional[Dict] = None) -> str:
    """Converte Markdown bold-italic (`***text***` ou `___text___`) para Unicode."""
    style = options.get('bold_italic_style', 'sans') if options else 'sans'
    mapping = UNICODE_BOLD_ITALIC
    if style == 'script':
        mapping = UNICODE_SCRIPT_BOLD

    def replace_bold_italic(match: re.Match) -> str:
        content = match.group(2)
        if not content or content.isspace():
            return match.group(0)
        converted_content = _convert_text(content, mapping)
        # Se a conversão não alterou o conteúdo, retorna o original com marcadores
        if converted_content == content:
            return match.group(0)
        return converted_content

    bold_italic_regex = r'(\*\*\*|___)(.+?)\1'
    return re.sub(bold_italic_regex, replace_bold_italic, text)

def convert_strikethrough(text: str, options: Optional[Dict] = None) -> str:
    """Converte Markdown strikethrough (`~~text~~`) para Unicode."""
    strikethrough_regex = r'~~(.+?)~~'
    # Não retorna o original se não houver conversão, pois strikethrough sempre se aplica
    return re.sub(strikethrough_regex, lambda m: _convert_strikethrough(m.group(1)), text)

def convert_blockquote(text: str, options: Optional[Dict] = None) -> str:
    """Converte Markdown blockquote (`> text`) para Unicode (prefixo)."""
    blockquote_regex = r'^(\s*)> (.*)'
    match = re.match(blockquote_regex, text)
    if match:
        indent = match.group(1)
        content = match.group(2)
        return f"{indent}▎ {content}"
    return text

def convert_unordered_list(text: str, options: Optional[Dict] = None) -> str:
    """Converte Markdown unordered list (`- text` ou `* text`) para Unicode."""
    ulist_regex = r'^(\s*)(\*|-)\s+(.*)'
    return re.sub(ulist_regex, r'\1• \3', text)

def convert_horizontal_line(text: str, options: Optional[Dict] = None) -> str:
    """Converte Markdown horizontal line (`---`, `***`, `___`) para Unicode."""
    hr_regex = r'^\s*(?:-{3,}|\*{3,}|_{3,})\s*$'
    if re.match(hr_regex, text):
        return '─' * 10
    return text

# --- Função Principal de Conversão ---

CONVERSION_PIPELINE: list[Callable[[str, Optional[Dict]], str]] = [
    convert_horizontal_line,
    convert_blockquote,
    convert_unordered_list,
    convert_bold_italic,
    convert_bold,
    convert_italic,
    convert_strikethrough,
]

def markdown_to_unicode(markdown_text: str, options: Optional[Dict] = None) -> str:
    """Converte uma string Markdown completa para Unicode.

    Args:
        markdown_text: O texto Markdown a ser convertido.
        options: Dicionário de opções de formatação (ex: {'bold_style': 'script'}).

    Returns:
        O texto convertido para Unicode.
    """
    lines = markdown_text.split('\n')
    unicode_lines = []
    for line in lines:
        processed_line = line
        original_line_state = processed_line # Salva estado antes de inline

        # Aplica conversões de bloco primeiro
        block_applied = False
        for convert_func in [convert_horizontal_line, convert_blockquote, convert_unordered_list]:
            new_line = convert_func(processed_line, options)
            if new_line != processed_line:
                processed_line = new_line
                block_applied = True
                break # Aplica apenas a primeira conversão de bloco que corresponder

        # Se não foi uma linha horizontal (que é um bloco terminal),
        # aplica conversões inline
        is_hr = (len(processed_line) == 10 and all(c == '─' for c in processed_line))
        if not is_hr:
            inline_pipeline = [convert_bold_italic, convert_bold, convert_italic, convert_strikethrough]
            for convert_func in inline_pipeline:
                processed_line = convert_func(processed_line, options)

        unicode_lines.append(processed_line)

    return '\n'.join(unicode_lines)

# --- Exemplo de Uso ---
if __name__ == '__main__':
    md_input = """
# Exemplo de Texto

Este é um **texto** com __negrito__.
Este é um *texto* com _itálico_.
Este é um ***texto*** com ___negrito e itálico___.
Este é um ~~texto tachado~~.
Este é um *123* e **456**.

  - Item de lista 1
  * Item de lista 2

> Isto é um blockquote.
> > Nested quote (não suportado ainda)

---

Texto normal após a linha.

**Opções de Estilo:**
Texto com **negrito sans**.
Texto com *itálico sans*.
Texto com ***negrito itálico sans***.
Texto com **_bold e italic_** (teste aninhado).
Texto com *__italic e bold__* (teste aninhado).
"""

    print("--- Conversão Padrão (Sans-Serif) ---")
    unicode_output_sans = markdown_to_unicode(md_input)
    print(unicode_output_sans)

    print("\n--- Conversão com Opções (Script) ---")
    script_options = {
        'bold_style': 'script',
        'italic_style': 'script',
        'bold_italic_style': 'script'
    }
    unicode_output_script = markdown_to_unicode(md_input, options=script_options)
    print(unicode_output_script)

    print("\n--- Teste Específico Blockquote e HR ---")
    md_test = "  > Linha de citação\n  ---"
    print(markdown_to_unicode(md_test))

    print("\n--- Teste Específico Lista ---")
    md_list = "  - Item A\n  * Item B"
    print(markdown_to_unicode(md_list))

