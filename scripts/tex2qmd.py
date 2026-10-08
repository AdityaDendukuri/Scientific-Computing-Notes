#!/usr/bin/env python3
"""Convert cs111 LaTeX subfiles to Quarto Markdown (.qmd).

Usage:
    python scripts/tex2qmd.py src/lu.tex direct-methods/lu.qmd
    python scripts/tex2qmd.py --all          # convert all tracked files
"""

import re
import sys
from pathlib import Path

# ── Brace extraction ─────────────────────────────────────────────────────────

def extract_arg(text: str, pos: int) -> tuple[str, int]:
    """Extract content of first {...} at or after pos. Returns (content, end_pos)."""
    while pos < len(text) and text[pos] != '{':
        pos += 1
    if pos >= len(text):
        return '', pos
    pos += 1  # skip opening '{'
    depth = 1
    start = pos
    while pos < len(text) and depth > 0:
        c = text[pos]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        pos += 1
    return text[start:pos - 1], pos


# ── Strip preamble ───────────────────────────────────────────────────────────

def strip_preamble(text: str) -> str:
    text = re.sub(r'\\documentclass\[.*?\]\{.*?\}\s*\n', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{document\}\s*\n?', '', text)
    text = re.sub(r'\\end\{document\}\s*\n?', '', text)
    text = re.sub(r'\\addcontentsline\{.*?\}\{.*?\}\{.*?\}', '', text)
    return text


# ── Section headings ─────────────────────────────────────────────────────────

def convert_sections(text: str) -> str:
    text = re.sub(r'\\section\*\{([^}]+)\}', r'# \1 {.unnumbered}', text)
    text = re.sub(r'\\section\*?\{([^}]+)\}', r'# \1', text)
    text = re.sub(r'\\subsection\*?\{([^}]+)\}', r'# \1', text)
    text = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'## \1', text)
    return text


# ── Math environments ────────────────────────────────────────────────────────

def convert_math(text: str) -> str:
    # \[...\] → $$...$$
    text = re.sub(r'\\\[\s*\n?(.*?)\n?\s*\\\]', r'$$\1$$', text, flags=re.DOTALL)
    # \begin{align}...\end{align} → wrapped in $$
    for env in ('align', 'align*', 'equation', 'equation*'):
        text = re.sub(
            r'\\begin\{' + re.escape(env) + r'\}(.*?)\\end\{' + re.escape(env) + r'\}',
            lambda m, e=env: (
                '$$\n\\begin{' + e.rstrip('*') + '}\n' + m.group(1).strip() + '\n\\end{' + e.rstrip('*') + '}\n$$'
                if 'align' in e else
                '$$\n' + m.group(1).strip() + '\n$$'
            ),
            text, flags=re.DOTALL
        )
    # \begin{pmatrix/bmatrix/vmatrix} — leave alone inside $$, Quarto/MathJax handles them
    return text


# ── Lists ────────────────────────────────────────────────────────────────────

def convert_lists(text: str) -> str:
    """Convert arbitrarily nested enumerate/itemize environments.

    Convert innermost environments first. When their parent is converted on a
    later pass, every continuation line is indented so the inner Markdown list
    remains attached to the correct outer item.
    """
    innermost = re.compile(
        r'\\begin\{(?P<env>enumerate|itemize)\}'
        r'(?P<body>(?:(?!\\begin\{(?:enumerate|itemize)\}).)*?)'
        r'\\end\{(?P=env)\}',
        flags=re.DOTALL,
    )

    def render_list(m: re.Match) -> str:
        marker = '1.' if m.group('env') == 'enumerate' else '-'
        parts = re.split(r'\\item(?:\s*\[[^]]*\])?\s*', m.group('body'))
        items = []
        for part in parts[1:]:
            lines = part.strip().splitlines()
            if not lines:
                continue
            rendered = [f'{marker} {lines[0]}']
            rendered.extend(('    ' + line) if line else '' for line in lines[1:])
            items.append('\n'.join(rendered))
        return '\n' + '\n\n'.join(items) + '\n'

    while True:
        text, count = innermost.subn(render_list, text)
        if count == 0:
            break
    return text


# ── Inline formatting ────────────────────────────────────────────────────────

def convert_formatting(text: str) -> str:
    def replace_one_arg(source: str, macro: str, left: str, right: str) -> str:
        result = []
        i = 0
        while i < len(source):
            if source.startswith(macro, i) and _is_word_end(source, i + len(macro)):
                j = i + len(macro)
                while j < len(source) and source[j].isspace():
                    j += 1
                if j < len(source) and source[j] == '{':
                    body, end = extract_arg(source, j)
                    result.append(left + body + right)
                    i = end
                    continue
            result.append(source[i])
            i += 1
        return ''.join(result)

    def replace_href(source: str) -> str:
        result = []
        i = 0
        macro = r'\href'
        while i < len(source):
            if source.startswith(macro, i) and _is_word_end(source, i + len(macro)):
                j = i + len(macro)
                while j < len(source) and source[j].isspace():
                    j += 1
                if j < len(source) and source[j] == '{':
                    url, end = extract_arg(source, j)
                    j = end
                    while j < len(source) and source[j].isspace():
                        j += 1
                    if j < len(source) and source[j] == '{':
                        label, end = extract_arg(source, j)
                        result.append(f'[{label}]({url})')
                        i = end
                        continue
            result.append(source[i])
            i += 1
        return ''.join(result)

    text = replace_href(text)
    for macro, left, right in (
        (r'\textbf', '**', '**'),
        (r'\textit', '*', '*'),
        (r'\emph', '*', '*'),
        (r'\texttt', '`', '`'),
    ):
        # Repeated passes also handle the same formatting command nested in itself.
        while macro in text:
            converted = replace_one_arg(text, macro, left, right)
            if converted == text:
                break
            text = converted
    return text


# ── Cross-references ─────────────────────────────────────────────────────────

def convert_references(text: str) -> str:
    text = re.sub(r'\\label\{[^}]+\}', '', text)
    text = re.sub(r'(?:Section|Sec\.?|\\S)~?\\ref\{[^}]+\}',
                  'the referenced section', text)
    text = re.sub(r'(?:Definition|Theorem|Lemma|Corollary|Proposition|Exercise|'
                  r'Def|Thm|Lem|Cor|Prop|Remark|Ex)\.?~?\\ref\{[^}]+\}',
                  'the referenced result', text)
    text = re.sub(r'\\eqref\{[^}]+\}', 'the referenced equation', text)
    text = re.sub(r'\\ref\{[^}]+\}', 'the referenced item', text)
    return text


def convert_citations(text: str) -> str:
    """Convert the citation forms used in the TeX sources to Pandoc citations."""
    def parenthetical(m: re.Match) -> str:
        keys = [key.strip() for key in m.group(1).split(',') if key.strip()]
        return '[' + '; '.join('@' + key for key in keys) + ']'

    def textual(m: re.Match) -> str:
        keys = [key.strip() for key in m.group(1).split(',') if key.strip()]
        if len(keys) == 1:
            return '@' + keys[0]
        return '[' + '; '.join('@' + key for key in keys) + ']'

    text = re.sub(r'\\citep\{([^}]+)\}', parenthetical, text)
    text = re.sub(r'\\cite\{([^}]+)\}', parenthetical, text)
    text = re.sub(r'\\citet\{([^}]+)\}', textual, text)
    return text


# ── Miscellaneous commands ────────────────────────────────────────────────────

def convert_verbatim(text: str) -> str:
    """Convert verbatim/lstlisting blocks to fenced code blocks."""
    def make_fence(m: re.Match) -> str:
        lang = m.group(1) if m.lastindex and m.group(1) else ''
        return '\n```' + lang.strip() + '\n' + m.group(2 if m.lastindex else 1).rstrip() + '\n```\n'

    # \begin{lstlisting}[language=X] ... \end{lstlisting}
    text = re.sub(
        r'\\begin\{lstlisting\}(?:\[language=(\w+)\])?\s*(.*?)\\end\{lstlisting\}',
        make_fence, text, flags=re.DOTALL)
    # \begin{verbatim} ... \end{verbatim}
    text = re.sub(
        r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',
        lambda m: '\n```\n' + m.group(1).rstrip() + '\n```\n',
        text, flags=re.DOTALL)
    return text


def convert_misc(text: str) -> str:
    text = text.replace(r'\square', r'\square')      # keep inside math
    text = text.replace(r'\checkmark', '✓')
    text = re.sub(r'\\(medskip|bigskip|smallskip|vspace\{[^}]+\}|vskip\s+\S+)', '\n', text)
    text = re.sub(r'\\newpage\b', '\n\n', text)
    text = re.sub(r'\\sectionend\b', '', text)
    text = re.sub(r'\\noindent\b\s*', '', text)
    text = re.sub(r'\\enspace\b', ' ', text)
    text = re.sub(r'\\hfill\b', '', text)
    text = re.sub(r'\\begin\{center\}(.*?)\\end\{center\}', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{flushright\}(.*?)\\end\{flushright\}', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'\\newentry\b', '', text)
    text = text.replace(r'\exCheck', '**Check.** ')
    text = text.replace(r'\exDerive', '**Derive.** ')
    text = text.replace(r'\exCompute', '**Compute.** ')
    text = text.replace(r'\exExplore', '**Explore.** ')
    text = re.sub(r'\\nocite\{\*\}', '', text)
    text = re.sub(r'\\bibliographystyle\{[^}]+\}', '', text)
    text = re.sub(
        r'\\bibliography\{[^}]+\}',
        '\n# References {.unnumbered}\n\n::: {#refs}\n:::\n',
        text,
    )
    text = re.sub(r'\\ldots\b', '...', text)
    text = re.sub(r'\\cdots\b', r'\\cdots', text)  # keep in math context
    text = re.sub(r'\\dots\b', '...', text)
    # \\ line breaks in text (not in math) → space
    # (leave \\ alone; inside align envs it is needed)
    return text


# ── Custom cs111 macro conversion ────────────────────────────────────────────

# Macros that take (title, body) — listed in order to try
TWO_ARG_MACROS = [
    ('\\addDef',  'callout-note',    'Definition'),
    ('\\addThm',  'callout-note',    'Theorem'),
    ('\\addLem',  'callout-note',    'Lemma'),
    ('\\addCor',  'callout-note',    'Corollary'),
    ('\\addProp', 'callout-note',    'Proposition'),
    ('\\addExmpl','callout-note',    'Example'),
    ('\\addTrail','callout-important','Literature trail'),
    ('\\addRoute','callout-note',    'Chapter route'),
]

ONE_ARG_MACROS = [
    ('\\addPrf',  'callout-tip',     'Proof',    True),   # collapse=true
    ('\\proofMap','callout-tip',     'Proof map', False),
    ('\\addReading','callout-note',  'Further reading', False),
    ('\\addRemark', 'callout-tip',   'Remark',   False),
    ('\\addExcr', 'callout-warning', 'Exercise', False),
    ('\\textBox', None,              None,       False),  # plain block
]


def _is_word_end(text: str, pos: int) -> bool:
    """Return True if position is not followed by another letter (macro name boundary)."""
    return pos >= len(text) or not text[pos].isalpha()


def _format_callout(callout: str, header: str | None, body: str, collapse: bool = False) -> str:
    body = body.strip().lstrip('%').strip()
    if callout is None:
        return '\n' + body + '\n'
    attrs = f'.{callout} icon=false'
    if collapse:
        attrs += ' collapse=true'
    lines = [f'\n::: {{{attrs}}}']
    if header:
        lines.append(f'## {header}')
    lines.append(body)
    lines.append(':::')
    return '\n'.join(lines) + '\n'


def convert_macros(text: str) -> str:
    """Scan text and replace all custom cs111 macros with Quarto callouts."""
    result = []
    i = 0
    n = len(text)

    while i < n:
        matched = False

        # Try two-arg macros
        for (macro, callout, label) in TWO_ARG_MACROS:
            mlen = len(macro)
            if text[i:i + mlen] == macro and _is_word_end(text, i + mlen):
                j = i + mlen
                # Skip optional \label{...} that sometimes appears between macro and args
                while j < n and text[j] in ' \t\n':
                    j += 1
                if text[j:j + 6] == '\\label':
                    _, j = extract_arg(text, j + 6)
                    while j < n and text[j] in ' \t\n':
                        j += 1

                title, j = extract_arg(text, j)
                title = title.strip().lstrip('%').strip()

                # Skip whitespace between args
                k = j
                while k < n and text[k] in ' \t\n':
                    k += 1

                # Check if a second arg follows
                if k < n and text[k] == '{':
                    body, j = extract_arg(text, k)
                    header = f'{label}: {title}' if title else label
                else:
                    # Only one arg — treat as body, use label as header
                    body = title
                    header = label
                    j = k

                result.append(_format_callout(callout, header, body))
                i = j
                matched = True
                break

        if matched:
            continue

        # Try one-arg macros
        for (macro, callout, label, collapse) in ONE_ARG_MACROS:
            mlen = len(macro)
            if text[i:i + mlen] == macro and _is_word_end(text, i + mlen):
                j = i + mlen
                body, j = extract_arg(text, j)
                result.append(_format_callout(callout, label, body, collapse))
                i = j
                matched = True
                break

        if not matched:
            result.append(text[i])
            i += 1

    return ''.join(result)


# ── Clean up residual LaTeX ───────────────────────────────────────────────────

def cleanup(text: str) -> str:
    # Strip remaining unknown \commands that take no visible argument
    text = re.sub(r'\\(?:mLabel|refstepcounter|newentry|setlength|renewcommand)\{[^}]*\}(?:\{[^}]*\})*', '', text)
    # Generated Markdown should never carry TeX spacing as trailing whitespace.
    text = '\n'.join(line.rstrip() for line in text.splitlines())
    # Collapse 3+ blank lines to 2
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = text.strip()
    # Remove leading '---' lines — Quarto reads them as unclosed YAML front matter
    while text.startswith('---'):
        text = text[3:].lstrip('\n')
    text = text.strip() + '\n'
    return text


# ── Main conversion pipeline ─────────────────────────────────────────────────

def convert(tex_text: str, title: str = '', sec_label: str = '') -> str:
    nocite_all = r'\nocite{*}' in tex_text
    text = strip_preamble(tex_text)
    text = convert_verbatim(text)     # before macros so verbatim content is protected
    text = convert_macros(text)       # must come before formatting (preserves braces in macro args)
    text = convert_sections(text)
    text = convert_math(text)
    text = convert_lists(text)
    text = convert_formatting(text)
    text = convert_citations(text)
    text = convert_references(text)
    text = convert_misc(text)
    text = cleanup(text)

    # Prepend YAML front-matter if title provided
    if title:
        label = sec_label or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        front = f'# {title} {{#sec-{label}}}\n\n'
        text = front + text

    if nocite_all:
        text = '---\nnocite: |\n  @*\n---\n\n' + text

    return text


# ── File mapping ──────────────────────────────────────────────────────────────

FILE_MAP = [
    # (src tex, output qmd, page title, section label)
    # Preface
    ('src/preface.tex',         'index.qmd',                              '',               ''),

    # Chapter 1: Fundamentals
    ('src/math_notation.tex',   'fundamentals/math-notation.qmd',         '',               ''),
    ('src/vecs_and_mats.tex',   'fundamentals/vectors-matrices.qmd',      '',               ''),
    ('src/norms_intro.tex',     'fundamentals/norms.qmd',                 '',               ''),
    ('src/complexity.tex',      'fundamentals/complexity.qmd',            '',               ''),
    ('src/floating_point.tex',  'fundamentals/floating-point.qmd',        '',               ''),
    ('src/numpy_primer.tex',    'fundamentals/numpy-primer.qmd',          '',               ''),

    # Chapter 2: Direct Methods
    ('src/linear_systems.tex',  'direct-methods/linear-systems.qmd',      '',               ''),
    ('src/lu.tex',              'direct-methods/lu.qmd',                  '',               ''),
    ('src/spd.tex',             'direct-methods/spd.qmd',                 '',               ''),
    ('src/structured_solvers.tex', 'direct-methods/structured-solvers.qmd', '',             ''),

    # Chapter 3: Orthogonality and Least Squares
    ('src/orthogonal.tex',      'orthogonality/orthogonal.qmd',           '',               ''),
    ('src/norm.tex',            'orthogonality/norms.qmd',                '',               ''),
    ('src/stability.tex',       'orthogonality/stability.qmd',            '',               ''),
    ('src/least_squares.tex',   'orthogonality/least-squares.qmd',        '',               ''),

    # Chapter 4: Eigenvalues and SVD
    ('src/eigen.tex',           'eigenvalues/eigenvalues.qmd',            '',               ''),
    ('src/eigen_algorithms.tex', 'eigenvalues/eigen-algorithms.qmd',      '',               ''),
    ('src/svd.tex',             'eigenvalues/svd.qmd',                    '',               ''),
    ('src/arnoldi.tex',         'eigenvalues/arnoldi.qmd',                '',               ''),
    ('src/lanczos.tex',         'eigenvalues/lanczos.qmd',                '',               ''),

    # Chapter 5: Iterative Methods
    ('src/iterative.tex',       'iterative/iterative.qmd',                '',               ''),
    ('src/jacobi.tex',          'iterative/jacobi.qmd',                   '',               ''),
    ('src/conj_grad.tex',       'iterative/conjugate-gradient.qmd',       '',               ''),
    ('src/gmres.tex',           'iterative/gmres.qmd',                    '',               ''),
    ('src/randomized.tex',      'iterative/randomized.qmd',               '',               ''),
    ('src/multigrid.tex',       'iterative/multigrid.qmd',                '',               ''),

    # Chapter 6: Numerical Analysis
    ('src/interpolation.tex',   'numerical-analysis/interpolation.qmd',   '',               ''),
    ('src/chebyshev.tex',       'numerical-analysis/chebyshev.qmd',       '',               ''),
    ('src/quadrature.tex',      'numerical-analysis/quadrature.qmd',      '',               ''),

    # Chapter 7: ODEs
    ('src/ode_methods.tex',     'odes/ode-methods.qmd',                   '',               ''),

    # Chapter 8: Applications
    ('src/pca.tex',             'applications/pca.qmd',                   '',               ''),
    ('src/graphs.tex',          'applications/graphs.qmd',                '',               ''),
    ('src/operators.tex',       'applications/operators.qmd',             '',               ''),
    ('src/fourier.tex',         'applications/fourier.qmd',               '',               ''),
    ('src/matrix_exponential.tex', 'applications/matrix-exponential.qmd', '',               ''),
    ('src/markov.tex',          'applications/markov.qmd',                '',               ''),
    ('src/koopman.tex',         'applications/koopman.qmd',               '',               ''),
    ('src/references.tex',       'references.qmd',                         '',               ''),
]


def convert_all(root: Path) -> None:
    for src_rel, dst_rel, title, label in FILE_MAP:
        src = root / src_rel
        dst = root / dst_rel
        if not src.exists():
            print(f'  SKIP  {src_rel}  (not found)')
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        tex = src.read_text(encoding='utf-8')
        qmd = convert(tex, title, label)
        dst.write_text(qmd, encoding='utf-8')
        print(f'  OK    {src_rel}  →  {dst_rel}')


def main() -> None:
    root = Path(__file__).parent.parent  # repo root

    if len(sys.argv) == 2 and sys.argv[1] == '--all':
        print('Converting all files...')
        convert_all(root)
        print('Done.')
        return

    if len(sys.argv) == 3:
        src = Path(sys.argv[1])
        dst = Path(sys.argv[2])
        if not src.is_absolute():
            src = root / src
        if not dst.is_absolute():
            dst = root / dst
        dst.parent.mkdir(parents=True, exist_ok=True)
        tex = src.read_text(encoding='utf-8')
        qmd = convert(tex)
        dst.write_text(qmd, encoding='utf-8')
        print(f'Written: {dst}')
        return

    print(__doc__)
    sys.exit(1)


if __name__ == '__main__':
    main()
