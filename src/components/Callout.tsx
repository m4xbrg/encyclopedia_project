import { type ReactNode, useId } from 'react';
import styles from './Callout.module.css';

type CalloutType = 'note' | 'proof' | 'warning';

type CalloutProps = {
  type: CalloutType;
  title?: string;
  children: ReactNode;
};

const DEFAULT_TITLES: Record<CalloutType, string> = {
  note: 'Note',
  proof: 'Proof',
  warning: 'Warning',
};

const ICONS: Record<CalloutType, ReactNode> = {
  note: (
    <svg viewBox="0 0 24 24" role="img" aria-hidden="true" width="20" height="20">
      <path
        fill="currentColor"
        d="M12 2a10 10 0 1 0 10 10A10.011 10.011 0 0 0 12 2Zm.75 14.5h-1.5v-5h1.5Zm0-7h-1.5v-2h1.5Z"
      />
    </svg>
  ),
  proof: (
    <svg viewBox="0 0 24 24" role="img" aria-hidden="true" width="20" height="20">
      <path
        fill="currentColor"
        d="M10.5 15.586 7.707 12.793l1.414-1.414L10.5 12.758l4.379-4.379 1.414 1.414Z"
      />
    </svg>
  ),
  warning: (
    <svg viewBox="0 0 24 24" role="img" aria-hidden="true" width="20" height="20">
      <path
        fill="currentColor"
        d="M1 21h22L12 2Zm12-3h-2v-2h2Zm0-4h-2v-4h2Z"
      />
    </svg>
  ),
};

function roleForType(type: CalloutType) {
  return type === 'warning' ? 'alert' : 'note';
}

export default function Callout({ type, title, children }: CalloutProps) {
  const titleId = useId();
  const resolvedTitle = title ?? DEFAULT_TITLES[type];

  return (
    <section
      className={`${styles.callout} ${styles[type]}`}
      role={roleForType(type)}
      tabIndex={0}
      aria-labelledby={titleId}
    >
      <span className={styles.iconWrapper} aria-hidden="true">
        {ICONS[type]}
      </span>
      <div>
        <p id={titleId} className={styles.title}>
          {resolvedTitle}
        </p>
        <div className={styles.body}>{children}</div>
      </div>
    </section>
  );
}
