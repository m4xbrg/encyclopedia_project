Formal Systems and Axiomatic Methods
ID: MATH.1.1
Domain: Foundations & Preliminaries
Topic: Mathematical Logic & Proof Techniques

```
[Axiomatic Set Theory]

\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic \& Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a branch of mathematical logic that formalizes the concept of sets through a series of axioms, providing a rigorous foundation for set-based mathematics. The most prominent system is Zermelo-Fraenkel Set Theory (ZF), which often includes the Axiom of Choice (ZFC).

\subsection*{Core Principles}
\begin{itemize}
  \item \textbf{Axiom of Extensionality:} Two sets are equal if they have the same elements.
  \item \textbf{Axiom of Empty Set:} There exists a set with no elements, denoted as $\varnothing$.
  \item \textbf{Axiom of Pairing:} For any two sets $a$ and $b$, there exists a set that contains exactly $a$ and $b$.
  \item \textbf{Axiom of Union:} For any set $A$, there exists a set containing all elements of the elements of $A$.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
    & \text{Let } A = \{ x \in U \mid P(x) \} \text{ denote the set of all elements } x \text{ in } U \text{ satisfying property } P.\\
    & A \cap B = \{ x \mid x \in A \text{ and } x \in B \}\\
    & A \cup B = \{ x \mid x \in A \text{ or } x \in B \}
\end{align*}

\subsection*{Worked Example}
Consider the sets \( A = \{1, 2\} \) and \( B = \{2, 3\} \). The intersection \( A \cap B = \{2\} \) and the union \( A \cup B = \{1, 2, 3\} \). These operations illustrate the axiomatic definitions in practice.

\subsection*{Common Pitfalls}
- Confusing the concepts of subsets and elements, where \( a \in A \) does not imply \( a \subseteq A \).
- Misapplying the Axiom of Choice in contexts where it is not necessary or relevant.

\subsection*{Connections}
Axiomatic Set Theory serves as the foundation for various mathematical disciplines, including topology, algebra, and the theory of functions. It is pivotal for understanding concepts such as cardinality and ordinals, along with foundational results in mathematical logic.

\subsection*{Further Reading}
- Cohen, P. J. (1963). *Set Theory and the Continuum Hypothesis*. 
- Jech, T. (2003). *Set Theory*. 
- Halmos, P. R. (1960). *Naive Set Theory*.
```