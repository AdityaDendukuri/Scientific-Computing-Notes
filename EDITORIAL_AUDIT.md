# Textbook Polish Audit

These notes should remain terse, but each chapter should be self-contained enough
that a motivated reader can learn from it without the missing lecture context.
The goal is not to make every chapter long. The goal is to add the missing
motivation, examples, assumptions, and interpretation that make each page
locally learnable.

## Editorial Standard

Each chapter should answer the following questions.

1. What problem or object is this chapter about?
1. Why does it matter computationally?
1. What assumptions are being made?
1. What are the central definitions, theorems, or algorithms?
1. What do the formulas mean in words?
1. What can go wrong numerically?
1. What is the smallest concrete example that makes the idea real?
1. How does this chapter connect to later material?

Preferred section pattern:

```markdown
# Topic

Short motivation paragraph.

## Main Idea

Plain-language explanation before formalism.

::: {.callout-note icon=false}
## Definition / Theorem / Algorithm
Formal statement.
:::

Interpretation paragraph.

::: {.callout-tip icon=false}
**Rule / Mental Model:** ...
:::

## Example

Small worked example.

## Numerical Notes

Cost, stability, conditioning, implementation cautions.
```

Every formal block should be followed by interpretation unless the meaning is
already immediate.

## Source-Of-Truth Note

The canonical source is LaTeX in `src/*.tex`. The pipeline converts TeX to
Quarto with `scripts/tex2qmd.py --all`, then renders downstream outputs. Edit
the TeX source first; generated `.qmd`, `_site`, HTML, and PDF outputs should be
treated as build artifacts unless a task explicitly targets the generator.

## Priority Order

First polish batch:

1. `src/floating_point.tex`
1. `src/linear_systems.tex`
1. `src/lu.tex`
1. `src/spd.tex`
1. `src/orthogonal.tex`
1. `src/stability.tex`
1. `src/least_squares.tex`
1. `src/svd.tex`
1. `src/eigen.tex`
1. `src/iterative.tex`
1. `src/conj_grad.tex`
1. `src/gmres.tex`
1. `src/operators.tex`
1. `src/ode_methods.tex`

After the spine is stronger, polish the remaining applications and advanced
topics.

## Preface

Canonical source: `src/preface.tex`

Missing concepts:

- How to read the notes.
- Prerequisites: linear algebra, calculus, Python/NumPy.
- A map of the subject: floating point, linear systems, orthogonality,
  eigenvalues, iterative methods, numerical analysis, applications.
- Clarification that the notes are now aiming to be a compact self-study text,
  not only a CS111 study guide.

Suggested additions:

- Add a short "How to Use These Notes" section.
- Add a "Mathematical Spine" paragraph explaining why linear algebra is the
  organizing principle.
- Add a "Reader Contract" paragraph: terse definitions, examples, exercises,
  and numerical warnings.

## Fundamentals

### Mathematical Notation and Proof Techniques

Canonical source: `src/math_notation.tex`

Missing concepts:

- Quantifier examples in numerical contexts.
- Difference between exact equality, approximation, asymptotic equality, and
  numerical equality.
- Row/column and index conventions.
- One-indexed mathematical notation vs zero-indexed Python notation.

Suggested chapter flow:

1. Logic and quantifiers.
1. Sets and functions.
1. Equality, approximation, and asymptotic notation.
1. Index notation and summation.
1. Proof techniques.
1. Notation conventions used in the book.

Concrete additions:

- Example translating "for every tolerance there exists a grid size" into
  symbols.
- Small table: `=`, `\approx`, `O(...)`, `\sim`, `\lesssim`.

### Vectors and Matrices

Canonical source: `src/vecs_and_mats.tex`

Missing concepts:

- Matrix-vector multiplication as a linear combination of columns.
- Rows as measurements and columns as directions.
- Four views of a matrix: linear map, data table, system of equations, basis
  transformation.
- Shape discipline: checking dimensions before doing algebra.
- Translation between mathematical vectors and NumPy arrays.

Suggested additions:

- Add a "Four Views of a Matrix" section.
- Add a worked example showing `A @ x` as a column combination.
- Add a shape-checking callout before matrix arithmetic.

### Matrix Arithmetic

Canonical source: `src/arithmetic.tex`

Missing concepts:

- Why matrix multiplication is defined by rows against columns.
- Matrix multiplication as composition of linear maps.
- Inner product vs outer product.
- Blocking/cache intuition for real performance.
- Difference between flop count and wall-clock time.

Suggested additions:

- Add a conceptual bridge before the definition of matrix multiplication.
- Add a small example comparing `(AB)x` and `A(Bx)`.
- Add a "Computation vs Algebra" note near cost analysis.

### Introduction to Norms

Canonical source: `src/norms_intro.tex`

Missing concepts:

- Why norms are needed before discussing error and convergence.
- Absolute, relative, and normwise error.
- Geometric meaning of `l1`, `l2`, and `linf`.
- What norm equivalence does and does not say computationally.
- Connection to stopping criteria.

Suggested additions:

- Add a "Norms Measure Error" section.
- Add geometric examples for common vector norms.
- Add a warning that constants in norm equivalence may depend on dimension.

### Computational Complexity

Canonical source: `src/complexity.tex`

Missing concepts:

- Big-O vs constants.
- Flops vs memory bandwidth.
- Dense vs sparse complexity.
- Setup cost vs repeated solve cost.
- Why `O(n^3)` is the central dense linear algebra barrier.

Suggested additions:

- Add a table of common dense costs: matvec, matrix multiply, LU, QR, SVD.
- Add a short sparse contrast: matvec is often `O(nnz)`.
- Add a note that asymptotics do not predict small problem performance.

### Floating Point Arithmetic

Canonical source: `src/floating_point.tex`

Missing concepts:

- More worked examples of cancellation, absorption, overflow, and underflow.
- Clear bridge from floating-point error to forward/backward stability.
- Floating-point comparisons and tolerances.
- Why summation order matters.
- Stable rewrites such as `log1p`, `expm1`, `hypot`, and compensated summation.
- Explicit distinction between machine epsilon and unit roundoff.

Suggested chapter flow:

1. Why real numbers cannot be stored exactly.
1. IEEE representation and spacing.
1. Machine epsilon vs unit roundoff.
1. The fundamental rounding model.
1. Arithmetic pathologies.
1. Measuring error.
1. Stable rewrites and practical rules.
1. Bridge to conditioning and stability.

Concrete additions:

- Example: `(1e16 + 1) - 1e16`.
- Example: quadratic formula cancellation and stable alternative.
- Example: naive sum vs pairwise or compensated sum.
- Callout: use `np.isclose`, not `==`, for most computed real values.

### Python and NumPy Primer

Canonical source: `src/numpy_primer.tex`

Missing concepts:

- `(n,)` vs `(n, 1)` vs `(1, n)` arrays.
- Broadcasting rules.
- Views vs copies.
- `@` vs `*`.
- `np.linalg.solve(A, b)` vs `np.linalg.inv(A) @ b`.
- Brief mention of SciPy sparse arrays.

Suggested additions:

- Add a "Shape Discipline" section.
- Add a table of common linear algebra calls.
- Add a warning about silent broadcasting.

## Direct Methods

### Linearity

Canonical source: `src/linear_systems.tex`

Missing concepts:

- Consistent, inconsistent, underdetermined, and overdetermined systems.
- Rank as the number of independent constraints.
- Geometry of `Ax=b` as intersecting hyperplanes.
- Range/nullspace interpretation of solvability.
- Residual `r=b-Ax`.
- Exact solution vs least-squares solution.

Suggested chapter flow:

1. Linear systems as matrix equations.
1. Geometry of equations and unknowns.
1. Existence and uniqueness.
1. Rank, nullspace, and range.
1. Residuals and approximate solutions.
1. Four fundamental subspaces.

Concrete additions:

- Add a 2-by-2 consistent example and an inconsistent example.
- Add a rank-deficient system with infinitely many solutions.
- Add a callout defining residuals before least squares appears later.

### LU Factorization

Canonical source: `src/lu.tex`

Missing concepts:

- Full worked Gaussian elimination example.
- Elimination matrices.
- Pivoting as avoiding division by small numbers.
- Partial vs complete pivoting.
- Growth factor intuition.
- Reuse for many right-hand sides.
- Factorization cost vs triangular solve cost.

Suggested chapter flow:

1. Why triangular systems are easy.
1. Gaussian elimination as factorization.
1. Worked elimination example.
1. Forward/back substitution.
1. Pivoting and stability.
1. Cost and reuse.

Concrete additions:

- Add a 3-by-3 worked LU example.
- Add a tiny unstable no-pivot example with a small pivot.
- Add a table: factor once, solve many times.

### Symmetric Positive Definite Matrices

Canonical source: `src/spd.tex`

Missing concepts:

- SPD geometry: ellipsoids and energy.
- Positive definite vs positive semidefinite.
- Eigenvalue, quadratic form, and principal minor tests.
- Why SPD enables Cholesky.
- Why SPD is the setting for CG.
- Examples: covariance matrices, normal equations, Poisson matrices.

Suggested chapter flow:

1. Symmetry and quadratic forms.
1. Positive definiteness.
1. Geometry and energy.
1. Equivalent tests.
1. Cholesky.
1. Why SPD matters computationally.

Concrete additions:

- Add a 2D ellipse example for `x^T A x = 1`.
- Add an SPSD covariance example.
- Add a "Where SPD appears" callout.

## Orthogonality And Least Squares

### Orthogonal Matrices

Canonical source: `src/orthogonal.tex`

Missing concepts:

- Orthogonal transformations as rotations and reflections.
- Why orthogonal matrices are numerically safe.
- Classical vs modified Gram-Schmidt vs Householder.
- Loss of orthogonality in finite precision.
- Thin QR vs full QR.
- QR as change of basis.

Suggested additions:

- Add a rotation/reflection example.
- Add a "Why QR is stable" bridge before QR.
- Add comparison table: CGS, MGS, Householder.

### Vector and Matrix Norms

Canonical source: `src/norm.tex`

Missing concepts:

- How this chapter differs from the introductory norms chapter generated from
  `src/norms_intro.tex`.
- Induced matrix norm derivation.
- Spectral norm as maximum stretching.
- Frobenius norm as Euclidean norm of entries.
- Normwise vs componentwise error.
- Which norms appear in which algorithms.

Suggested additions:

- Add an opening note: this chapter extends norms to linear maps.
- Add examples computing `1`, `infty`, Frobenius, and spectral norms.
- Add a table of where each norm is used.

### Stability and Condition Number

Canonical source: `src/stability.tex`

Missing concepts:

- Forward error, backward error, and residual compared explicitly.
- Small residual does not imply small error.
- Algorithm stability vs problem conditioning.
- Stable algorithm plus ill-conditioned problem distinction.
- Backward stability examples: QR, Householder, GEPP.
- Iterative refinement limitations.

Suggested chapter flow:

1. Residual, forward error, backward error.
1. Conditioning is about the problem.
1. Stability is about the algorithm.
1. Why inverses are avoided.
1. Solver selection hierarchy.
1. Iterative refinement.

Concrete additions:

- Add a 2-by-2 ill-conditioned example where residual is small but error is
  large.
- Add a two-column table: "problem property" vs "algorithm property".

### Overdetermined Systems and Least Squares

Canonical source: `src/least_squares.tex`

Missing concepts:

- Projection theorem before normal equations.
- Geometry of residual orthogonal to column space.
- Normal equations as derivation, not default algorithm.
- QR vs SVD decision rule.
- Rank-deficient least squares.
- Weighted least squares.
- Connection to regression.

Suggested additions:

- Add a "Projection View" section before normal equations.
- Add a method comparison table: normal equations, QR, SVD.
- Add rank-deficient example using the pseudoinverse.

### Chebyshev Polynomials

Canonical source: `src/chebyshev.tex`

Missing concepts:

- Approximation vs interpolation.
- Why monomial basis is computationally bad.
- Chebyshev nodes vs Chebyshev basis.
- Minimax property intuition.
- Mapping `[a,b]` to `[-1,1]`.
- Connection to spectral methods.

Suggested additions:

- Add a "Two Problems with Monomials" section.
- Add an interval mapping formula.
- Add a short note connecting Chebyshev series to Fourier cosine series.

## Eigenvalues And SVD

### Eigenvalues and Eigenvectors

Canonical source: `src/eigen.tex`

Missing concepts:

- Eigenvectors as invariant directions.
- Algebraic vs geometric multiplicity.
- Defective matrices.
- Diagonalization vs Schur decomposition.
- Why characteristic polynomials are not used numerically.
- Power iteration failure modes.
- Shifted inverse iteration intuition.
- QR algorithm as the practical dense eigenvalue method.

Suggested additions:

- Add a geometric opening example.
- Add a "Do not compute eigenvalues from the characteristic polynomial" warning.
- Add comparison table: power, inverse, RQI, QR.

### Singular Value Decomposition

Canonical source: `src/svd.tex`

Missing concepts:

- Full, thin, and economy SVD.
- Geometric picture: rotate, stretch, rotate.
- Rank, numerical rank, and singular value decay.
- Conditioning through singular values.
- Pseudoinverse for rank-deficient systems.
- SVD as the universal fallback method.
- Examples: image compression, least squares, PCA.

Suggested chapter flow:

1. What SVD decomposes geometrically.
1. Full and thin SVD.
1. Singular values, rank, and conditioning.
1. Fundamental subspaces.
1. Low-rank approximation.
1. Pseudoinverse.
1. Applications.

Concrete additions:

- Add a table of SVD shapes for `m >= n`.
- Add a numerical rank callout using a tolerance.
- Add a small image/data compression explanation.

### Lanczos Algorithm

Canonical source: `src/lanczos.tex`

Missing concepts:

- Why Krylov subspaces approximate extreme eigenvalues.
- Relation to power iteration.
- Tridiagonal projection meaning.
- Ritz values and Ritz vectors explained slowly.
- Loss of orthogonality and ghost eigenvalues.
- Reorthogonalization.
- Symmetric-only assumption.

Suggested additions:

- Add a "Power Iteration With Memory" framing.
- Add a diagram-in-words: large matrix projected to small tridiagonal matrix.
- Add a finite-precision warning section.

### Jacobi Eigenvalue Algorithm

Canonical source: `src/jacobi_eig.tex`

Missing concepts:

- Why zeroing off-diagonal entries reveals eigenvalues.
- Givens rotation geometry.
- Off-diagonal norm as convergence measure.
- Comparison with QR algorithm.
- When Jacobi is still useful.

Suggested additions:

- Add a 2-by-2 rotation example.
- Add a "Convergence Measure" section.
- Add a note: accurate for symmetric matrices but usually not the fastest dense
  method.

## Iterative Methods

### Iterative Methods for Linear Systems

Canonical source: `src/iterative.tex`

Missing concepts:

- Why direct methods fail at scale.
- Sparse matrices and matrix-free matvecs.
- Fixed-point iteration framing.
- Residual vs error in stopping criteria.
- Spectral radius intuition.
- Preconditioning preview.

Suggested chapter flow:

1. Direct vs iterative at scale.
1. Matrix-vector products as the primitive.
1. Fixed-point iterations.
1. Convergence and spectral radius.
1. Residuals and stopping.
1. Sparse storage and preconditioning.

Concrete additions:

- Add a large sparse Poisson example as motivation.
- Add a residual/error warning that links conceptually to stability.

### Jacobi and Gauss-Seidel Methods

Canonical source: `src/jacobi.tex`

Missing concepts:

- Matrix splitting `A=M-N`.
- Jacobi/Gauss-Seidel as fixed-point methods.
- Why Gauss-Seidel uses fresh updates.
- Diagonal dominance intuition.
- SOR parameter choice and sensitivity.
- These methods as smoothers, not usually final solvers.

Suggested additions:

- Add a shared splitting derivation.
- Add a small 3-by-3 iteration example.
- Add a multigrid smoother note.

### Conjugate Gradient Method

Canonical source: `src/conj_grad.tex`

Missing concepts:

- CG as minimization of a quadratic energy.
- Why SPD is essential.
- Residual orthogonality vs search direction conjugacy.
- Polynomial approximation view.
- Finite precision behavior.
- Practical stopping tests.
- Preconditioning as standard usage, not an add-on.

Suggested chapter flow:

1. SPD systems and energy minimization.
1. Steepest descent limitation.
1. Conjugate directions.
1. Krylov subspaces.
1. The CG recurrence.
1. Convergence and spectrum.
1. Preconditioning and stopping.

Concrete additions:

- Add a "CG only applies to SPD systems" warning.
- Add a comparison to steepest descent.
- Add stopping criterion `||r_k|| / ||b|| <= tol`.

### GMRES

Canonical source: `src/gmres.tex`

Missing concepts:

- Why CG does not apply to nonsymmetric systems.
- Arnoldi process intuition.
- Krylov basis storage cost.
- Why GMRES solves a small least-squares problem.
- Restarting: memory benefit vs convergence loss.
- Preconditioning conventions: left and right.
- Breakdown and stagnation.

Suggested chapter flow:

1. Nonsymmetric systems and the loss of CG structure.
1. Krylov approximation.
1. Arnoldi orthogonalization.
1. Residual minimization.
1. Hessenberg least squares.
1. Restarting.
1. Preconditioning and failure modes.

Concrete additions:

- Add a "CG vs GMRES" comparison table.
- Add a paragraph explaining why storage grows with iteration count.
- Add a warning that restarted GMRES can stagnate.

## Numerical Analysis

### Polynomial Interpolation

Canonical source: `src/interpolation.tex`

Missing concepts:

- Interpolation vs approximation.
- Polynomial uniqueness proof intuition.
- Lagrange basis interpretation.
- Barycentric formula as stable evaluation.
- Runge phenomenon from high degree and bad node choice.
- Splines as local polynomial interpolation.
- Error formula and dependence on the node polynomial.

Suggested additions:

- Add a "What interpolation promises" opening.
- Add a small three-point Lagrange example.
- Add an error formula section before Runge's phenomenon.

### Numerical Quadrature

Canonical source: `src/quadrature.tex`

Missing concepts:

- Quadrature as interpolation followed by integration.
- Degree of exactness.
- Composite vs single-panel rules.
- Smoothness assumptions behind error rates.
- Endpoint singularities.
- Adaptive quadrature decision logic.
- Monte Carlo quadrature as contrast.

Suggested additions:

- Add a "Quadrature From Interpolation" section.
- Add degree-of-exactness examples for trapezoid and Simpson.
- Add a warning about nonsmooth integrands and singular endpoints.

### Root Finding

Canonical source: `src/root_finding.tex`

Missing concepts:

- Bracketing vs open methods as a decision tree.
- Fixed-point iteration view.
- Multiplicity and slow convergence.
- Newton basins and dependence on initial guesses.
- Stopping criteria: residual small vs step small.
- Secant method derivation.
- Brent's method as practical default.

Suggested additions:

- Add a method decision table.
- Add Newton failure examples: zero derivative and poor initial guess.
- Add stopping criteria section.

## ODEs

### Numerical Methods for ODEs

Canonical source: `src/ode_methods.tex`

Missing concepts:

- IVP vs BVP distinction.
- Local truncation error vs global error.
- Stability regions.
- Stiffness definition and examples.
- Explicit vs implicit tradeoff.
- Adaptive error control details.
- Symplectic integrators and long-time energy behavior.
- Connection between ODE solvers and Newton/linear solves.

Suggested chapter flow:

1. Initial value problems.
1. Error: local vs global.
1. Forward and backward Euler.
1. Stability and stiffness.
1. Runge-Kutta methods.
1. Adaptive step size.
1. Symplectic methods.
1. Practical solver selection.

Concrete additions:

- Add test equation `y' = lambda y` as the running stability example.
- Add stiff example with fast decay and slow dynamics.
- Add solver selection note: explicit RK for nonstiff, implicit for stiff.

## Applications

### Principal Component Analysis

Canonical source: `src/pca.tex`

Missing concepts:

- Data matrix convention: rows are samples, columns are features.
- Centering vs standardization.
- Scores vs loadings in words.
- PCA as rotation that diagonalizes covariance.
- PCA as best low-rank approximation.
- Interpretation limits: components are not necessarily causal.
- Small worked example.

Suggested additions:

- Add a data matrix convention callout.
- Add a tiny centered dataset example.
- Add a warning about scale and interpretability.

### Spectral Graph Theory and PageRank

Canonical source: `src/graphs.tex`

Missing concepts:

- Directed vs undirected conventions.
- Row-stochastic vs column-stochastic consistency.
- Laplacian quadratic form intuition.
- Connected components and nullspace.
- Normalized Laplacian motivation.
- Spectral clustering relaxation explained more carefully.
- PageRank dangling nodes.

Suggested additions:

- Add a convention callout for graph direction and stochastic matrices.
- Add a 3-node graph example.
- Add a dangling-node warning in PageRank.

### Linear Operators and the Poisson Equation

Canonical source: `src/operators.tex`

Missing concepts:

- Function spaces at an intuitive level.
- Boundary conditions.
- Discretization as replacing operators with matrices.
- Grid spacing and consistency.
- Poisson equation physical interpretation.
- Why Laplacian matrices are sparse and SPD.
- Conditioning growth with mesh refinement.

Suggested chapter flow:

1. Operators as infinite-dimensional matrices.
1. Boundary value problems.
1. Finite differences.
1. The discrete Laplacian.
1. Spectrum and conditioning.
1. Solving Poisson systems.

Concrete additions:

- Add a "grid function" definition.
- Add Dirichlet boundary condition explanation.
- Add note: `kappa(T) = O(h^{-2})` for the 1D Laplacian.

### Fourier Analysis as Change of Basis

Canonical source: `src/fourier.tex`

Missing concepts:

- Complex exponentials as rotating basis vectors.
- Frequency bins and ordering.
- Normalization conventions.
- Aliasing and Nyquist frequency.
- Periodicity assumptions.
- FFT recursion explained visually or algebraically.
- Convolution theorem with a small example.

Suggested additions:

- Add a "Frequencies on a finite grid" section.
- Add a normalization convention note.
- Add a small circular convolution example.

### Markov Chains and Stochastic Matrices

Canonical source: `src/markov.tex`

Missing concepts:

- Probability vector convention.
- Column-stochastic vs row-stochastic note.
- Reducible and periodic chains.
- Stationary distribution examples.
- Spectral gap as convergence rate.
- Detailed balance intuition.
- Metropolis-Hastings derivation is currently too fast.

Suggested additions:

- Add a convention callout at the top.
- Add two-state chain examples.
- Add reducible and periodic counterexamples.

### Koopman Theory, DMD, and SINDy

Canonical source: `src/koopman.tex`

Missing concepts:

- Simple nonlinear map example.
- Observable examples.
- Why Koopman is linear but infinite-dimensional.
- Difference between state dynamics and observable dynamics.
- DMD as finite-dimensional least-squares approximation.
- SINDy as equation discovery, not modal decomposition.
- Noise, derivative estimation, and library choice caveats.

Suggested chapter flow:

1. Nonlinear dynamics and observables.
1. Koopman operator.
1. Why linear but infinite-dimensional matters.
1. DMD as finite-dimensional approximation.
1. SINDy as sparse equation discovery.
1. Practical caveats.

Concrete additions:

- Add example `x_{k+1} = x_k^2` and observables `g(x)=x`, `g(x)=x^2`.
- Add comparison table: DMD vs SINDy.
- Add warning about noisy derivatives in SINDy.
