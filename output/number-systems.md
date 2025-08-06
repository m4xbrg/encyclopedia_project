\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a foundational framework in mathematics that formalizes the notion of set using axioms. The most prominent examples include Zermelo-Fraenkel set theory (ZF) and Zermelo-Fraenkel set theory with the Axiom of Choice (ZFC). In this context, a set is typically denoted by curly braces, with the notation \( x \in A \) indicating that \( x \) is an element of the set \( A \).

\subsection*{Core Principles}
\begin{itemize}
  \item **Axiom of Extensionality**: Two sets are equal if they have the same elements.
  \item **Axiom of Pairing**: For any two sets, there exists a set that contains exactly those two sets.
  \item **Axiom of Union**: For any set, there exists a set that contains all the elements of the elements of that set.
  \item **Axiom of Separation**: Given a set and a property, there exists a subset containing exactly those elements that satisfy the property.
  \item **Axiom of Infinity**: There exists a set that contains the empty set and is closed under the operation of forming singletons.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
  &A = \{x \in U \mid P(x)\} \quad \text{(Subset defined by property } P\text{)} \\
  &\forall x \in A, \, \exists y \in A: y \in x \quad \text{(Axiom of Union)}
\end{align*}

\subsection*{Worked Example}
Consider the set \( A = \{1, 2, 3\} \). By the Axiom of Pairing, we can form the set \( B = \{A, A\} = \{\{1, 2, 3\}, \{1, 2, 3\}\} \). This construction shows how pairs are formed within the axiomatic framework.

\subsection*{Common Pitfalls}
Learners often confuse sets with their elements, mistakenly asserting that a set can be an element of itself, which violates the Axiom of Regularity. Additionally, the independence of the Axiom of Choice is frequently misunderstood, leading to confusion regarding its necessity in certain set-theoretic contexts.

\subsection*{Connections}
Axiomatic Set Theory serves as the foundation for most mathematical theories, connecting deeply with concepts such as functions, relations, and cardinality. It also provides the framework for higher-level areas such as model theory and category theory.

\subsection*{Further Reading}
For a deeper understanding of Axiomatic Set Theory, consult "Set Theory: An Introduction to Independence" by Kenneth Kunen and "Naive Set Theory" by Paul R. Halmos. These texts provide essential insights and comprehensive discussions surrounding the axioms and their implications.