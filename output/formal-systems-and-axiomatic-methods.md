Formal Systems and Axiomatic Methods
ID: MATH.1.1
Domain: Foundations & Preliminaries
Topic: Mathematical Logic & Proof Techniques

\section*{Axiomatic Set Theory}
\subsection*{Domain} Mathematical Logic & Foundations
\subsection*{Subfield} Set Theory

\subsection*{Definition}
Axiomatic Set Theory is a branch of mathematical logic that formalizes the concept of a set through a collection of axioms. These axioms serve as the foundational rules governing the manipulation and existence of sets within the mathematical framework. A prominent example is Zermelo-Fraenkel set theory (ZF), which includes the Axiom of Extensionality and the Axiom of Choice.

\subsection*{Core Principles}
\begin{itemize}
  \item \textbf{Axiom of Extensionality:} Two sets are equal if they have the same elements.
  \item \textbf{Axiom of Pairing:} For any two sets, there exists a set containing exactly those two sets.
  \item \textbf{Axiom of Union:} For any set, there exists a set that contains all the elements of the sets contained in it.
  \item \textbf{Axiom of Infinity:} There exists a set that contains the empty set and is closed under the operation of forming the successor.
  \item \textbf{Axiom of Choice:} For any set of non-empty sets, there exists a choice function that selects one element from each set.
\end{itemize}

\subsection*{Key Formulas or Symbolic Representations}
\begin{align*}
  S \in T & \iff \text{set } S \text{ is an element of set } T, \\
  S_1 = S_2 & \iff \forall x (x \in S_1 \iff x \in S_2).
\end{align*}

\subsection*{Worked Example}
Consider the set \( A = \{1, 2\} \) and \( B = \{ \{1\}, \{2\} \} \). According to the Axiom of Pairing, the set \( \{A, B\} \) exists, containing exactly the sets \( A \) and \( B \). To verify equality, we check if \( A = B \), noting that \( 1 \notin B \) and \( \{1\} \notin A \); hence \( A \neq B \).

\subsection*{Common Pitfalls}
Learners often confuse sets with their elements, misapply the Axiom of Choice, or overlook the implications of set equality under the Axiom of Extensionality. Additionally, they may fail to recognize that not all intuitive collections are sets, as some may lead to paradoxes.

\subsection*{Connections}
Axiomatic Set Theory forms the backbone of much of modern mathematics, interfacing with topology, analysis, and algebra. It presupposes familiarity with logic and foundational principles. Further, it serves as a reference point for alternative set theories, such as naive set theory and non-standard models.

\subsection*{Further Reading}
For an in-depth exploration of Axiomatic Set Theory, refer to:
- Cohen, P. J., \textit{Set Theory and the Continuum Hypothesis} (1966).
- Jech, T. J., \textit{Set Theory} (2003).
- Suppes, P., \textit{Axiomatic Set Theory} (1960).