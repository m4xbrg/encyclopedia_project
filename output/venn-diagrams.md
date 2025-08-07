Venn Diagrams
ID: MATH.1.2
Domain: Foundations & Preliminaries
Topic: Set Theory & Foundations

```
[Axiomatic Set Theory]

\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic set theory is a formalized framework for constructing set theory using a set of axioms from which theorems can be derived. These axioms serve as foundational statements regarding the properties and relationships of sets. 

\subsection*{Core Principles}
\begin{itemize}
  \item **Axiom of Extensionality**: Two sets are equal if and only if they have the same elements.
  \item **Axiom of Pairing**: For any two sets, there exists a set that contains exactly these two sets.
  \item **Axiom of Union**: For any set, there exists a set that contains all elements of the elements of the first set.
  \item **Axiom of Power Set**: For any set, there exists a set of all its subsets.
  \item **Axiom of Infinity**: There exists a set that contains the empty set and is closed under the operation of forming singleton sets.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
\forall A, B (A = B \iff \forall x (x \in A \iff x \in B)) \quad & (\text{Axiom of Extensionality}) \\
\exists C \forall x (x \in C \iff x = a \lor x = b) \quad & (\text{Axiom of Pairing}) \\
\exists U \forall x (x \in U \iff \exists y (y \in A \land x \in y)) \quad & (\text{Axiom of Union}) \\
\exists P \forall x (x \in P \iff x \subseteq A) \quad & (\text{Axiom of Power Set}) \\
\exists I (\emptyset \in I \land \forall x (x \in I \rightarrow (x \cup \{x\} \in I))) \quad & (\text{Axiom of Infinity})
\end{align*}

\subsection*{Worked Example}
Consider the set \( A = \{ 1, 2, 3 \} \). By the Axiom of Pairing, we can form the set \( B = \{ A, A \} \) which includes the set \( A \) itself as an element. The Union Axiom guarantees the existence of a set \( U \) such that \( U = 1 \cup 2 \cup 3 \), demonstrating the merger of initial elements.

\subsection*{Common Pitfalls}
- Confusing set equality with the equality of their individual elements.
- Assuming the existence of sets without properly applying the axioms.
- Misunderstanding the distinction between sets and their elements.

\subsection*{Connections}
Axiomatic set theory underpins many areas of mathematics, establishing a rigorous foundation for concepts such as functions, relations, and cardinality. It is often a prerequisite for advanced studies in mathematical logic and topology.

\subsection*{Further Reading}
- Zermelo, E. (1908). \"A New Approach to the Foundations of Set Theory.\" 
- Cohen, P. J. (1966). \"Set Theory and the Continuum Hypothesis.\"
- Jech, T. (2003). \"Set Theory.\" Springer.
```