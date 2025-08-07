Propositional Logic
ID: MATH.1.1
Domain: Foundations & Preliminaries
Topic: Mathematical Logic & Proof Techniques

```
[Axiomatic Set Theory]

\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic set theory is a branch of mathematical logic that formalizes the concept of set through a collection of axioms. It aims to provide a rigorous foundation for mathematics by defining which sets exist and how they can be manipulated. The most prominent axiomatic systems include Zermelo-Fraenkel set theory (ZF) and ZF with the Axiom of Choice (ZFC).

\subsection*{Core Principles}
\begin{itemize}
  \item **Axiom of Extensionality**: Two sets are equal if they have the same elements.
  \item **Axiom of Pairing**: For any two sets, there exists a set that contains exactly those two sets.
  \item **Axiom of Union**: For any set, there exists a set that contains all elements of the elements of the initial set.
  \item **Axiom of Infinity**: There exists a set that contains the empty set and is closed under the operation of adding singletons.
  \item **Axiom of Power Set**: For any set, there exists a set of all its subsets.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
& \text{Let } x, y \in \mathcal{P}(A) \implies x = y \text{ if } \forall z (z \in x \iff z \in y) \quad \text{(Extensionality)} \\
& \{x, y\} = \{z \mid z = x \lor z = y\} \quad \text{(Pairing)} \\
& \bigcup A = \{x \mid \exists y (x \in y \land y \in A)\} \quad \text{(Union)} \\
& \mathcal{P}(A) = \{B \mid B \subseteq A\} \quad \text{(Power Set)}
\end{align*}

\subsection*{Worked Example}
Consider the set \( A = \{1, 2\} \). According to the Axiom of Pairing, the set \( \{1, 2\} \) can be constructed as the set of its elements \( 1 \) and \( 2 \). Additionally, applying the Axiom of Union, we can determine \( \bigcup \{A\} = \{1, 2\} \) since both elements of the set are included.

\subsection*{Common Pitfalls}
- Confusing the notion of a set with its elements, leading to incorrect applications of the Axiom of Extensionality.
- Misapplying axioms such as assuming the existence of infinite sets without using the Axiom of Infinity.
- Overlooking the distinction between a set and the property defining its members.

\subsection*{Connections}
Axiomatic set theory is foundational to various domains in mathematics, including number theory, topology, and analysis. It intersectly relates with concepts like functions, relations, and cardinality, which further build upon set-theoretic principles. Understanding these axioms is crucial for delving into mathematical proofs and the structure of mathematical systems.

\subsection*{Further Reading}
- Cohen, P. J. (1963). *Set Theory and the Continuum Hypothesis.*
- Zermelo, E. (1908). "Über die Grundlagen der Mengenlehre." *Mathematische Annalen.*
- Enderton, H. B. (1977). *Elements of Set Theory.*
```