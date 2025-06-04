# Conversor Markdown para Unicode em Python

Este projeto é uma reimplementação em Python do repositório [markdown-to-unicode](https://convert-md-to-uni.streamlit.app/), com funcionalidades adicionais.

## Funcionalidades

Converte as seguintes sintaxes Markdown para seus equivalentes em caracteres Unicode:

*   **Negrito:** `**texto**` ou `__texto__`
*   *Itálico:* `*texto*` ou `_texto_`
*   ***Negrito e Itálico:*** `***texto***` ou `___texto___`
*   ~~Tachado:~~ `~~texto~~`
*   Lista não ordenada: `- item` ou `* item` (converte para `• item`)
*   Blockquote: `> texto` (converte para `▎ texto`)
*   Linha Horizontal: `---`, `***`, ou `___` (converte para `──────────`)

## Funcionalidades Adicionais (Comparado ao Original JS)

*   **Blockquote:** Suporte para conversão de blockquotes.
*   **Linha Horizontal:** Suporte para conversão de linhas horizontais.
*   **Listas Não Ordenadas:** Conversão de marcadores `-` e `*` para `•`.
*   **Type Hints:** O código Python utiliza type hints para melhor clareza e manutenção (similar ao propósito do TypeScript).
*   **Opções de Estilo (Fontes):** Permite escolher diferentes estilos Unicode para negrito, itálico e negrito-itálico através de um dicionário de opções. Estilos disponíveis atualmente:
    *   `sans` (padrão): Sans-serif
    *   `script`: Estilo caligráfico (Script)

## Como Usar

O script principal é `converter.py`. Ele pode ser importado como um módulo ou executado diretamente para ver exemplos.

```python
from converter import markdown_to_unicode

markdown_input = """
Texto com **negrito** e *itálico*.
> Um blockquote.
---
- Item de lista.
"""

# Conversão padrão (estilo sans-serif)
unicode_output = markdown_to_unicode(markdown_input)
print(unicode_output)

# Conversão com estilo script
options = {
    'bold_style': 'script',
    'italic_style': 'script',
    'bold_italic_style': 'script'
}
unicode_output_script = markdown_to_unicode(markdown_input, options=options)
print(unicode_output_script)
```

## Executando os Testes

Os testes unitários estão localizados no diretório `tests/`. Para executá-los, navegue até o diretório raiz do projeto (`markdown_to_unicode_py`) e execute:

```bash
python3 -m unittest tests/test_converter.py
```

## Limitações Conhecidas

*   **Caracteres Suportados:** A conversão para estilos Unicode (negrito, itálico, script) funciona primariamente para letras ASCII (A-Z, a-z) e números (0-9 para negrito sans-serif). Caracteres acentuados e outros símbolos não são convertidos para esses estilos, mas são mantidos no texto.
*   **Números em Estilos:**
    *   Negrito Sans-Serif (`sans`): Suporta números (𝟬-𝟵).
    *   Itálico (`sans`, `script`): Não há caracteres Unicode padrão para números itálicos nesses estilos. Números dentro de marcadores de itálico (`*123*`) serão mantidos como estão, incluindo os marcadores.
    *   Negrito-Itálico (`sans`, `script`): Não há caracteres Unicode padrão para números negrito-itálico. Números dentro de marcadores (`***123***`) serão convertidos para **negrito** (se disponível, como em `sans`) e os marcadores de itálico restantes (`*`) serão mantidos: `*𝟭𝟮𝟯*`.
*   **Aninhamento Complexo:** O pipeline de conversão atual processa as marcações em uma ordem específica (bloco, depois inline do mais específico para o menos). Isso funciona bem para casos simples, mas pode não lidar corretamente com aninhamentos complexos como `**texto com _itálico_ dentro**` ou `*texto com __negrito__ dentro*`. Nesses casos, a formatação interna pode não ser aplicada como esperado.
*   **Outras Sintaxes Markdown:** Funcionalidades como code blocks (`, ```), links (`[texto](url)`), imagens (`![alt](url)`) e listas ordenadas não são suportadas nesta versão.

## Estrutura do Projeto

```
markdown_to_unicode_py/
├── converter.py       # Script principal com a lógica de conversão
├── tests/
│   └── test_converter.py # Testes unitários
└── README.md          # Este arquivo
```

