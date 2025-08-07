Predicate Logic
ID: MATH.1.1
Domain: Foundations & Preliminaries
Topic: Mathematical Logic & Proof Techniques

```
[Axiomatic Set Theory]

\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic \& Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a formal framework for set theory that defines set membership and operations through a collection of axioms. It aims to establish a rigorous foundation for mathematical reasoning concerning sets. The most widely used axiomatic systems include Zermelo-Fraenkel set theory with the Axiom of Choice (ZFC).

\subsection*{Core Principles}
\begin{itemize}
  \item Axiom of Extensionality: Two sets are equal if they have the same elements.
  \item Axiom of Pairing: For any two sets, there exists a set containing exactly those two sets.
  \item Axiom of Union: For any set, there exists a set that is the union of its elements.
  \item Axiom of Power Set: For any set, there exists a set of all of its subsets.
  \item Axiom of Infinity: There exists a set that contains the natural numbers.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
& \text{Extensionality: } \forall A \forall B \left( \forall x (x \in A \iff x \in B) \implies A = B \right) \\
& \text{Power Set: } \mathcal{P}(A) = \{ B \mid B \subseteq A \}
\end{align*}

\subsection*{Worked Example}
Consider the set \( A = \{1, 2\} \). By the Axiom of Pairing, the set \( \{ A, \{A\} \} \) is formed containing \( A \) and its singleton \( \{A\} \). Consequently, the operation of forming the union, \( \bigcup \{ A, \{A\} \} \), yields \( \{ 1, 2 \} \).

\subsection*{Common Pitfalls}
- Confusing the notion of a set with that of its elements.
- Assuming the existence of sets without reference to the axioms that guarantee them.
- Misunderstanding the concept of infinite sets and their construction.

\subsection*{Connections}
Axiomatic Set Theory serves as the foundation for much of modern mathematics, linking disparate fields through defined notations and established properties of sets. It forms the basis for advanced topics such as category theory and model theory. 

\subsection*{Further Reading}
- Kunen, K. (1980). *Set Theory: An Introduction to Independence*.
- Jech, T. (2003). *Set Theory*.
- Halmos, P. R. (1960). *Naive Set Theory*.
```