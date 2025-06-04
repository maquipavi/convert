import streamlit as st

# --- Lógica de Conversão do Repositório Original ---
# (Copiado de main.py)

tabela = {
    "=>": "⇒",  # Seta direita dupla
    "->": "→",  # Seta direita simples
    "<-": "←",  # Seta esquerda simples
    "<=>": "⇔", # Seta dupla com ponta nas duas direções
    "<->": "↔", # Seta simples com ponta nas duas direções
    "!=": "≠",  # Diferente de
    "<=": "≤",  # Menor ou igual a
    ">=": "≥",  # Maior ou igual a
    "==": "≡",  # Idêntico a / Equivalente
    "~=": "≅",  # Aproximadamente igual a
    "~~": "≈",  # Aproximadamente
    "!~": "≉",  # Não aproximadamente
    "v": "∨",   # OU lógico
    "^": "∧",   # E lógico
    "not": "¬", # Negação lógica
    "forall": "∀", # Para todo
    "exists": "∃", # Existe
    "in": "∈",  # Pertence a
    "notin": "∉", # Não pertence a
    "subset": "⊂", # Subconjunto próprio
    "subseteq": "⊆", # Subconjunto
    "supset": "⊃", # Superconjunto próprio
    "supseteq": "⊇", # Superconjunto
    "union": "∪",  # União de conjuntos
    "inter": "∩",  # Interseção de conjuntos
    "times": "×", # Produto cartesiano / multiplicação
    "prop": "∝", # Proporcional a
    "infty": "∞", # Infinito
    "sum": "∑",  # Somatório
    "prod": "∏", # Produtório
    "int": "∫",  # Integral
    "oint": "∮", # Integral de contorno fechado
    "grad": "∇", # Nabla / Gradiente
    "del": "∂",  # Derivada parcial
    "sqrt": "√", # Raiz quadrada
    "cbrt": "∛", # Raiz cúbica
    "deg": "°",  # Grau (ângulo/temperatura)
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "delta": "δ",
    "epsilon": "ε",
    "zeta": "ζ",
    "eta": "η",
    "theta": "θ",
    "iota": "ι",
    "kappa": "κ",
    "lambda": "λ",
    "mu": "μ",
    "nu": "ν",
    "xi": "ξ",
    "pi": "π",
    "rho": "ρ",
    "sigma": "σ",
    "tau": "τ",
    "upsilon": "υ",
    "phi": "φ",
    "chi": "χ",
    "psi": "ψ",
    "omega": "ω",
    "Gamma": "Γ",
    "Delta": "Δ",
    "Theta": "Θ",
    "Lambda": "Λ",
    "Xi": "Ξ",
    "Pi": "Π",
    "Sigma": "Σ",
    "Upsilon": "Υ",
    "Phi": "Φ",
    "Psi": "Ψ",
    "Omega": "Ω",
    "and": "∧",
    "or": "∨",
    "not": "¬",
    "::": "÷", # Divisão
    "approx": "≈",
    "equiv": "≡",
    "neq": "≠",
    "leq": "≤",
    "geq": "≥",
    "subsetneq": "⊂", # Subconjunto próprio (alternativa)
    "supsetneq": "⊃", # Superconjunto próprio (alternativa)
}

def replace_multiple(text, replacement_dict):
    """
    Substitui múltiplas substrings em uma string.

    Args:
        text (str): A string original.
        replacement_dict (dict): Um dicionário onde as chaves são as substrings a serem
                                 substituídas e os valores são as substituições.

    Returns:
        str: A string com as substituições aplicadas.
    """
    # É uma boa prática ordenar por comprimento decrescente para evitar
    # substituições parciais (e.g., substituir '->' antes de '>')
    # No entanto, para manter a lógica exata do repo original que não ordena,
    # vamos iterar diretamente sobre o dicionário. Se houver problemas,
    # reconsidere adicionar a ordenação:
    # sorted_replacements = sorted(replacement_dict.items(), key=lambda x: len(x[0]), reverse=True)
    # new_text = text
    # for old, new in sorted_replacements:
    #     new_text = new_text.replace(old, new)
    # return new_text

    # Lógica copiada diretamente do main.py original (sem ordenação)
    new_text = text
    for old, new in replacement_dict.items():
        new_text = new_text.replace(old, new)
    return new_text


# --- Interface Streamlit ---

st.title("Conversor Markdown para Unicode")

st.write("Cole seu texto que utiliza os símbolos definidos no repositório ")
st.markdown("[maquipavi/convert](https://github.com/maquipavi/convert)")
st.write("abaixo para converter para caracteres Unicode.")

input_text = st.text_area("Texto de entrada (Markdown):", height=200)

# Realiza a conversão automaticamente quando o texto de entrada muda
if input_text:
    output_text = replace_multiple(input_text, tabela)
    st.subheader("Texto convertido (Unicode):")
    st.text(output_text) # Use st.text para exibir como texto simples