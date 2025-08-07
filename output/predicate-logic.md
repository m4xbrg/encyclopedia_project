Predicate Logic
ID: MATH.1.1
Domain: Foundations & Preliminaries
Topic: Mathematical Logic & Proof Techniques

\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a formal framework within Set Theory that establishes the properties and relations of sets through a system of axioms rather than through intuitive or informal arguments. Prominent examples include Zermelo-Fraenkel Set Theory (ZF) and its extension with the Axiom of Choice (ZFC).

\subsection*{Core Principles}
\begin{itemize}
  \item \textbf{Axiom of Extensionality:} Two sets are equal if they have the same elements.
  \item \textbf{Axiom of Pairing:} For any sets \(a\) and \(b\), there exists a set that contains exactly \(a\) and \(b\).
  \item \textbf{Axiom of Union:} For any set \(A\), there exists a set that contains all the elements of the sets in \(A\).
  \item \textbf{Axiom of Infinity:} There exists a set that contains the empty set and is closed under the operation of taking the union with a singleton set.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
  & \text{If } a = b \text{ then } \forall x (x \in a \leftrightarrow x \in b) \\
  & \exists c \forall x (x \in c \leftrightarrow x = a \lor x = b) \\
  & \text{If } A \text{ is a set, then } \bigcup A = \{ x \mid \exists y (x \in y \land y \in A) \}
\end{align*}

\subsection*{Worked Example}
Consider the sets \(A = \{1, 2\}\) and \(B = \{2, 3\}\). By the Axiom of Pairing, we can form a new set \(C = \{A, B\}\). According to the Axiom of Union, the union of these sets is \(C \cup (A \cup B) = \{1, 2, 3\}\).

\subsection*{Common Pitfalls}
- Misunderstanding the Axiom of Extensionality can lead to incorrect conclusions about set equality.
- Assuming properties of sets without validating through axioms can result in flawed arguments.
- Overlooking the distinction between sets and their elements may lead to confusion in operations involving unions or intersections.

\subsection*{Connections}
Axiomatic Set Theory provides a foundational basis for various branches of mathematics, allowing the formalization of functions, relations, and numbers. It is closely linked to topics in Mathematical Logic such as model theory and proof theory, facilitating a deeper understanding of mathematical structures.

\subsection*{Further Reading}
- Zermelo, E. (1930). "The Axiomatic Foundations of Set Theory."
- Cohen, P. J. (1966). "Set Theory and the Continuum Hypothesis."
- Halmos, P. R. (1960). "Naive Set Theory."