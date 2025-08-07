\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a formal system that establishes the foundations of set theory through a fixed set of axioms, which serve as the basis for deducing theorems about sets. Usual formulations include the Zermelo-Fraenkel axioms with the Axiom of Choice, collectively denoted as ZFC.

\subsection*{Core Principles}
\begin{itemize}
  \item Axioms of Extensionality: Sets are equal if they contain the same elements.
  \item Axiom of Pairing: For any two sets, there exists a set that contains exactly those two sets.
  \item Axiom of Union: For any set, there exists a set containing all elements of its elements.
  \item Axiom of Power Set: For any set, there exists a set of all its subsets.
  \item Axiom of Infinity: Asserts the existence of an infinite set.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
  \text{Extensionality:} & \quad \forall A, B \left( \forall x \left( x \in A \iff x \in B \right) \Rightarrow A = B \right) \\
  \text{Pairing:} & \quad \forall x, y \exists z \forall w \left( w \in z \iff w = x \lor w = y \right) \\
  \text{Union:} & \quad \forall A \exists B \forall x \left( x \in B \iff \exists y (x \in y \land y \in A) \right)
\end{align*}

\subsection*{Worked Example}
Consider the sets \( A = \{1, 2\} \) and \( B = \{3\} \). By the Axiom of Pairing, we can construct the set \( C = \{A, B\} \). Thus, \( C = \{\{1, 2\}, \{3\}\} \) contains precisely the two sets as its elements.

\subsection*{Common Pitfalls}
Students often confuse sets with sequences, misinterpret the power set as simply listing elements, or overlook the implications of the Axiom of Choice in discussions around infinitude.

\subsection*{Connections}
Axiomatic Set Theory is foundational for various areas in mathematics, including arithmetic, topology, and analysis. It is also intrinsically linked to mathematical logic, particularly in understanding the properties of formal systems and their consistency.

\subsection*{Further Reading}
\begin{itemize}
  \item Cohen, P. J. (1966). Set Theory and the Continuum Hypothesis. W. A. Benjamin.
  \item Jech, T. (2003). Set Theory. Springer.
  \item Gödel, K. (1938). Consistency of the Axiom of Choice and the Generalized Continuum Hypothesis. Princeton University Press.
\end{itemize}