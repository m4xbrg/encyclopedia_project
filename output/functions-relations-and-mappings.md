Functions, Relations, and Mappings
ID: MATH.1.2
Domain: Foundations & Preliminaries
Topic: Set Theory & Foundations

\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a formalized framework in which set theory is grounded on a collection of axioms, designed to avoid paradoxes and ambiguities intrinsic to naive set theory. The axioms define how sets are constructed and relate to one another within a rigorous logical system.

\subsection*{Core Principles}
\begin{itemize}
  \item \textbf{Zermelo-Fraenkel Axioms (ZF)}: A common foundation, comprising axioms such as Extensionality, Pairing, Union, and the Power Set axiom.
  \item \textbf{Axiom of Choice (AC)}: Often included to establish the existence of choice functions on sets, leading to the Zermelo-Fraenkel Set Theory with Choice (ZFC).
  \item \textbf{Foundation Axiom}: Ensures sets do not contain themselves, preventing circular definitions.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
\forall A \, \forall B \, (A = B \iff \forall x \, (x \in A \iff x \in B)) & \quad \text{(Axiom of Extensionality)}\\
\{x, y\} & \quad \text{(Notation for a set containing elements } x \text{ and } y)\\
\mathcal{P}(A) & \quad \text{(Power Set of } A\text{, the set of all subsets of } A)
\end{align*}

\subsection*{Worked Example}
Consider the set \(A = \{1, 2\}\). The power set \(\mathcal{P}(A)\) consists of all subsets of \(A\), which are \(\{\}, \{1\}, \{2\}, \{1, 2\}\). This construction illustrates how the Power Set axiom functions in generating sets from existing collections.

\subsection*{Common Pitfalls}
- Misunderstanding the nature of infinity; mistakenly believing all sets can be constructed within finite operations.
- Confusing the concept of a set with that of its elements, particularly when discussing singleton sets or subsets.

\subsection*{Connections}
Axiomatic Set Theory serves as the backbone of modern mathematics, linking with various topics such as category theory, model theory, and the foundations of number systems. It underpins results in mathematical analysis and topology, highlighting its foundational role in broader mathematical frameworks.

\subsection*{Further Reading}
- Cohen, P. J. (1966). "Set Theory and the Continuum Hypothesis." Benjamin.
- Jech, T. (2003). "Set Theory." Springer.
- Suppes, P. (1972). "Axiomatic Set Theory." Dover Publications.