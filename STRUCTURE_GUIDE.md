# Structural Authoring Guide

The TeX files in `src/` are the canonical source. The notes should read as a
step-by-step mathematical build, not as isolated facts.

## Buildup Rule

Every major definition, theorem, lemma, and exercise should either introduce a
new object or explicitly use a previous object.

Use labels for reusable objects:

```tex
\label{def:...}
\label{thm:...}
\label{lem:...}
\label{ex:...}
```

When a result depends on a previous result, say so in the first sentence:

```tex
Using Def~\ref{def:residual}, ...
By Thm~\ref{thm:orthogonal-invariance}, ...
Return to Ex~\ref{ex:normal-equations-conditioning}.
```

## Remarks vs Exercises

Remarks are for brief context that would interrupt the main line. They should
not contain derivations, warnings that can be discovered, or algorithm-choice
rules that students can justify.

Convert passive remarks into exercises when the reader can work through the
math:

```tex
\addExcr{%
\begin{enumerate}
  \item Starting from Thm~\ref{...}, prove ...
  \item Use the result to explain ...
\end{enumerate}
}
\label{ex:...}
```

## Remark Titles

Remark titles should be compact noun phrases:

```tex
\textbf{(Householder stability)}\enspace
\textbf{(Least squares solver hierarchy)}\enspace
```

Avoid sentence-style labels:

```tex
\textbf{Why Householder is stable.}\enspace
\textbf{Use normal equations for derivation, not as the default algorithm.}\enspace
```

## Exercises

Exercises should usually ask for one of:

- derive a displayed equation from a previous theorem;
- verify a theorem on a small concrete example;
- compare two algorithms using the same problem;
- explain a numerical failure using conditioning or stability;
- connect the current chapter to a previous definition.

Avoid standalone computational tasks unless they reinforce a named result.
