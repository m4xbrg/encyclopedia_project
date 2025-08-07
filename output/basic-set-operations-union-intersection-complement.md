Basic Set Operations (union, intersection, complement)
ID: MATH.1.2
Domain: Foundations & Preliminaries
Topic: Set Theory & Foundations

\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a formal system that seeks to define sets and their properties through a set of axioms. It provides a foundation for mathematics by elucidating the principles governing sets without reliance on intuitive concepts.

\subsection*{Core Principles}
\begin{itemize}
  \item **Axiom of Extensionality**: Two sets are identical if they have the same elements.
  \item **Axiom of Pairing**: For any two sets, there exists a set that contains exactly these two sets.
  \item **Axiom of Union**: For any set, there exists a set containing exactly the elements of the member sets.
  \item **Axiom of Power Set**: For any set, there exists a set of all its subsets.
  \item **Axiom of Infinity**: There exists a set that contains the empty set and is closed under the operation of adding a single element.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
\forall x \forall y (x = y \iff \forall z (z \in x \iff z \in y) ) & \quad \text{(Extensionality)} \\
\forall x \exists y \forall z (z \in y \iff z = x \lor z \in x) & \quad \text{(Pairing)} \\
\forall x \exists y \forall z (z \in y \iff \exists w (z \in w \land w \in x)) & \quad \text{(Union)} \\
\forall x \exists y \forall z (z \in y \iff z \subseteq x) & \quad \text{(Power Set)} \\
\exists x ( \varnothing \in x \land \forall y (y \in x \implies y \cup \{y\} \in x)) & \quad \text{(Infinity)}
\end{align*}

\subsection*{Worked Example}
Consider the sets \(A = \{1, 2\}\) and \(B = \{2, 3\}\). By the Axiom of Union, the union \(A \cup B\) yields the set \(\{1, 2, 3\}\). This demonstrates the utility of the Axiom of Union in constructing new sets.

\subsection*{Common Pitfalls}
- Misunderstanding the distinction between sets and their elements can lead to incorrect applications of axioms.
- Assuming that all sets can be explicitly constructed rather than accepting the existence axiom may result in erroneous conclusions about set existence.
- Confusing set equality with element-wise similarity, which arises from the Axiom of Extensionality.

\subsection*{Connections}
Axiomatic Set Theory serves as a foundational framework for various branches of mathematics, including topology and analysis. It underpins the study of relations, functions, and cardinality, necessitating a comprehension of logical foundations prior to exploring these areas.

\subsection*{Further Reading}
- Cohen, P. J. (1966). "Set Theory and the Continuum Hypothesis."
- Zermelo, E. (1930). "A Basis for Set Theory."
- Halmos, P. R. (1960). "Naive Set Theory."