\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a formal framework for the study of sets through a collection of axioms that govern the behavior and relationships of sets, thus providing a foundation for mathematical analysis and discourse. Notable systems include Zermelo-Fraenkel set theory (ZF) and Zermelo-Fraenkel set theory with the Axiom of Choice (ZFC).

\subsection*{Core Principles}
\begin{itemize}
  \item The Axiom of Extensionality: Two sets are equal if they have the same elements.
  \item The Axiom of Pairing: For any two sets, there exists a set containing exactly those two sets.
  \item The Axiom of Union: For any set, there exists a set that contains all elements that are members of the elements of the original set.
  \item The Axiom of Power Set: For any set, there exists a set of all subsets of that set.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
  & \text{If } A, B \in \mathcal{P}(C), \text{ then } A \cup B \in \mathcal{P}(C) \\
  & \forall x (x \in A \rightarrow x \in B) \Rightarrow A = B
\end{align*}

\subsection*{Worked Example}
Consider the sets $A = \{1, 2\}$ and $B = \{2, 1\}$. By the Axiom of Extensionality, we can determine that $A = B$ since they contain the same elements. This demonstrates the principle that set equality is determined solely by membership.

\subsection*{Common Pitfalls}
- Misunderstanding the distinction between elements and subsets, leading to incorrect assumptions about set inclusion.
- Confusing the axioms of set theory with properties that may not hold in all set systems.
- Misapplying the Axiom of Choice in situations where it does not necessarily apply.

\subsection*{Connections}
Axiomatic Set Theory serves as the foundation for various branches of mathematics, such as topology and abstract algebra. It relates closely to concepts like ordinals and cardinals, which extend the discussion of size and order in set relations.

\subsection*{Further Reading}
- Cohen, P. J. (1966). Set Theory and the Continuum Hypothesis.
- Jech, T. (2003). Set Theory.
- Halmos, P. R. (1960). Naive Set Theory.