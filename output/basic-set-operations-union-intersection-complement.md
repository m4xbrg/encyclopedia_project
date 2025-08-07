Basic Set Operations (union, intersection, complement)
ID: MATH.1.2
Domain: Foundations & Preliminaries
Topic: Set Theory & Foundations

```
[Axiomatic Set Theory]

\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a formal framework for defining sets and their properties through a series of axioms. It provides a foundation for mathematics by delineating the permissible operations on sets using precise logical statements.

\subsection*{Core Principles}
\begin{itemize}
  \item Axiom of Extensionality: Two sets are equal if they have the same elements.
  \item Axiom of Pairing: For any two sets, there exists a set that contains exactly those two sets.
  \item Axiom of Union: For any set, there exists a set that contains all elements of the sets in that set.
  \item Axiom of Power Set: For any set, there exists a set of all its subsets.
  \item Axiom of Infinity: There exists a set that contains the empty set and is closed under the operation of adding single elements.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
  A &= \{x \mid P(x)\} \text{ (Set builder notation)} \\
  A \subseteq B &\text{ if } \forall x (x \in A \Rightarrow x \in B) \\
  \mathcal{P}(A) &\text{ (Power set of } A\text{)}
\end{align*}

\subsection*{Worked Example}
Consider the set \( A = \{1, 2, 3\} \). By the Axiom of Pairing, one can form the set \( B = \{A, \{A\}\} \) which contains the set \( A \) and the singleton set \( \{A\} \). This illustrates the use of axioms to construct new sets from existing ones.

\subsection*{Common Pitfalls}
Students may confuse the Axiom of Extensionality with mere compositional understanding, mistakenly believing that order in a set matters. They might also overlook that a set can be defined by its properties rather than just its elements.

\subsection*{Connections}
Axiomatic Set Theory underpins various branches of mathematics including algebra and topology. It also serves as a prerequisite for understanding systems like Zermelo-Fraenkel Set Theory with the Axiom of Choice (ZFC) and its significance in the study of mathematical structures.

\subsection*{Further Reading}
For a thorough examination of Axiomatic Set Theory, refer to "Set Theory: An Introduction to Independence" by Kenneth Kunen and "Naive Set Theory" by Paul R. Halmos.
```