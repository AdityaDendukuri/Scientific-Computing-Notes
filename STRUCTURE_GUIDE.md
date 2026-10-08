# Structural Authoring Guide

The TeX files in `src/` are the canonical source. The notes should read as a
step-by-step mathematical build, not as isolated facts.

## Expository Lineage

The book combines three influences, in a deliberate order:

- **Meyer at the entrance:** begin with a concrete matrix, a computational
  question, and an example that makes the abstraction necessary.
- **Golub in the proof:** prefer constructive arguments from which a
  factorization, recurrence, or algorithm can be read directly.
- **Horn--Johnson at the horizon:** state exact hypotheses, collect useful
  equivalences, show what fails without an assumption, and point toward the
  deeper structure without making the entrance forbidding.

Do not blend all three levels into the opening paragraph. A chapter should
become more compressed and structural only after the reader knows the problem.

## Chapter Route

Every source chapter begins with `\\addRoute{question}{path}`. The question
should be concrete enough to motivate a calculation. The path should name the
mathematical sequence used to answer it. The route is a promise to the reader:
every major section should contribute to it.

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

## Proofs and Exercises

The main text should contain the proofs that carry the mathematical structure
of the course. In particular, include a proof when a result:

- explains why an algorithm works;
- connects algebraic structure to a numerical consequence;
- supplies a reusable error, stability, or optimality argument; or
- is needed to justify a later theorem.

Do not outsource such a proof to an exercise. After the proof, use an exercise
to verify the result on a small matrix, derive a corollary, test a limiting
case, or compare the theorem with computation. Short routine identities may
remain exercises when their solution introduces no new idea.

When a complete proof would require machinery outside the course, state the
needed hypotheses and label the argument as a proof outline. Do not present a
heuristic as a theorem proof.

Before a proof with more than one central idea, add a `\\proofMap{...}`. A
proof map names the ingredients and the order in which they are used; it does
not replace any step of the proof.

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

Use the following labels to make the expected kind of work visible:

- `\\exCheck` for a short calculation or direct verification;
- `\\exDerive` for a proof or symbolic development;
- `\\exCompute` for a sustained numerical calculation, implementation, or comparison;
- `\\exExplore` for interpretation, a counterexample, or an open extension.

Exercise sets should normally rise through these levels. Exercises should
usually ask for one of:

- derive a displayed equation from a previous theorem;
- verify a theorem on a small concrete example;
- compare two algorithms using the same problem;
- explain a numerical failure using conditioning or stability;
- connect the current chapter to a previous definition.

Avoid standalone computational tasks unless they reinforce a named result.

## Citing the Literature

Do not ask the reader to read a paper as an exercise. When a result comes from
the literature, state the result in the notes, give its hypotheses, explain
what it means for the computation, and cite the source with `\\citep{...}`.
If the proof is omitted, say so and cite where it can be found. Further
reading belongs in `\\addReading{...}` at the end of the chapter.

The main text remains self-contained. A cited result that is used later in the
core must be stated precisely where it is first needed.
