Venn Diagrams
ID: MATH.1.2
Domain: Foundations & Preliminaries
Topic: Set Theory & Foundations

\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic set theory is a formal framework in which the properties of sets are derived from a specified set of axioms. It provides a rigorous foundation for set theory and is used to avoid paradoxes associated with naive set definitions. Notably, it employs a formal language, typically first-order logic, to express the axioms and theorems.

\subsection*{Core Principles}
\begin{itemize}
  \item Axiom of Extensionality: Two sets are equal if and only if they have the same elements.
  \item Axiom of Regularity: Every non-empty set A contains an element that is disjoint from A.
  \item Axiom of Infinity: There exists a set that contains the empty set and is closed under the operation of forming unions.
  \item Axiom of Union: For any set A, there exists a set that is the union of all elements of A.
  \item Axiom Schema of Specification: For any set A, and any property P(x), there exists a subset of A containing exactly those elements of A that satisfy P.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
  & A = \{ x \mid P(x) \} \quad \text{(Set-builder notation)} \\
  & A \cap B = \{ x \mid x \in A \text{ and } x \in B \} \quad \text{(Intersection)} \\
  & A \cup B = \{ x \mid x \in A \text{ or } x \in B \} \quad \text{(Union)}
\end{align*}

\subsection*{Worked Example}
Consider a set \( A = \{1, 2, 3\} \). By the Axiom of Extensionality, another set \( B \) defined as \( B = \{3, 2, 1\} \) is equal to \( A \) since both sets contain the same elements. This illustrates that the order of elements does not affect set equality.

\subsection*{Common Pitfalls}
- Confusing the concept of set membership with subset relations.
- Misinterpreting the definition of an empty set and its properties.
- Assuming that sets can be defined through self-reference without regard for the Axiom of Regularity.

\subsection*{Connections}
Axiomatic set theory is foundational to various areas of mathematics, including topology, algebra, and analysis. It serves as a backdrop for discussing other mathematical structures, such as functions and relations, which rely on set-theoretic definitions. Understanding axiomatic set theory is crucial for engaging with more advanced topics like model theory and category theory.

\subsection*{Further Reading}
- Jech, T. J. (2003). *Set Theory*. Springer.
- Halmos, P. R. (1974). *Naive Set Theory*. Springer.
- Cohen, P. J. (1966). *Set Theory and the Continuum Hypothesis*. Addison-Wesley.