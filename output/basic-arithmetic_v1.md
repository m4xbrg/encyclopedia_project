\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a branch of set theory that formalizes the foundations of set theory through a set of axioms. The most prominent is the Zermelo-Fraenkel set theory (ZF), often supplemented by the Axiom of Choice (ZFC). In this framework, sets are syntactical objects defined by their properties and relationships rather than by construction.

\subsection*{Core Principles}
\begin{itemize}
  \item Axiom of Extensionality: Two sets are identical if they have the same elements.
  \item Axiom of Pairing: For any sets \(a\) and \(b\), there exists a set \(c\) that contains exactly \(a\) and \(b\).
  \item Axiom of Union: For any set \(A\), there exists a set that is the union of all elements of \(A\).
  \item Axiom of Power Set: For any set \(A\), there exists a set \(P(A)\) containing all subsets of \(A\).
  \item Axiom of Infinity: There exists a set that contains the empty set and is closed under the operation of forming singletons.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
  & \forall A, B \, (A = B \iff \forall x \, (x \in A \iff x \in B)) \quad \text{(Axiom of Extensionality)} \\
  & \forall a, b \, \exists c \, \forall x \, (x \in c \iff x = a \lor x = b) \quad \text{(Axiom of Pairing)} \\
  & \forall A \, \exists B \, \forall x \, (x \in B \iff \exists C \in A \, (x \in C)) \quad \text{(Axiom of Union)}
\end{align*}

\subsection*{Worked Example}
Consider the set \(A = \{1, 2\}\). By the Axiom of Pairing, we can form a set \(B\) containing only the elements of \(A\) and another set \(C\) containing the element \(3\). Thus, by the Axiom of Union, the union of sets \(A\) and \(C\) results in a set \(D = \{1, 2, 3\}\).

\subsection*{Common Pitfalls}
Learners frequently confuse the distinction between sets and elements, mistakenly treating a set as if it were one of its elements. Additionally, the assumption that all sets are definable can lead to paradoxical conclusions, such as Russell's Paradox.

\subsection*{Connections}
Axiomatic Set Theory connects to logic through its formal structure, serving as a foundational framework for various mathematical theories. It also relates to model theory and proof theory, extending into discussions of cardinality and the concepts of computability.

\subsection*{Further Reading}
- Cohen, P. J. (1963). "The Independence of the Continuum Hypothesis."
- Jech, T. (2003). "Set Theory" (3rd ed.).
- Suppes, P. (1972). "Axiomatic Set Theory."