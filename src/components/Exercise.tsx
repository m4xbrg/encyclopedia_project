import { type ReactNode, useId, useState } from 'react';
import styles from './Exercise.module.css';

type ExerciseProps = {
  prompt: ReactNode;
  hint: ReactNode;
  solution: ReactNode;
  label?: string;
};

export default function Exercise({ prompt, hint, solution, label = 'Exercise' }: ExerciseProps) {
  const hintId = useId();
  const solutionId = useId();
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);

  return (
    <section className={styles.exercise} aria-labelledby={`${hintId}-label`}>
      <p id={`${hintId}-label`} className={styles.header}>
        {label}
      </p>

      <div className={styles.prompt}>{prompt}</div>

      <div className={styles.actions}>
        <button
          type="button"
          className={styles.toggleButton}
          aria-expanded={showHint}
          aria-controls={hintId}
          onClick={() => setShowHint((current) => !current)}
        >
          {showHint ? 'Hide hint' : 'Show hint'}
        </button>

        <button
          type="button"
          className={styles.toggleButton}
          data-variant="secondary"
          aria-expanded={showSolution}
          aria-controls={solutionId}
          onClick={() => setShowSolution((current) => !current)}
        >
          {showSolution ? 'Hide solution' : 'Reveal solution'}
        </button>
      </div>

      <div id={hintId} role="region" aria-live="polite" hidden={!showHint} className={styles.panel}>
        <p className={styles.panelTitle}>Hint</p>
        <div>{hint}</div>
      </div>

      <div
        id={solutionId}
        role="region"
        aria-live="polite"
        hidden={!showSolution}
        className={styles.panel}
      >
        <p className={styles.panelTitle}>Solution</p>
        <div>{solution}</div>
      </div>
    </section>
  );
}
