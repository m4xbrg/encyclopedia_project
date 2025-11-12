import type { ChangeEvent, CSSProperties, FormEvent } from 'react';
import { useEffect, useMemo, useState } from 'react';

type SubjectOption = {
  label: string;
  value: string;
};

export type HeaderProps = {
  /** Text that appears next to the logo glyph */
  logoText?: string;
  /** List of subjects a reader can jump between */
  subjects?: SubjectOption[];
  /** Currently active subject value */
  selectedSubject?: string;
  /** Notified whenever the subject dropdown changes */
  onSubjectChange?: (nextValue: string) => void;
  /** Optional callback for the search form */
  onSearch?: (query: string) => void;
  /** Text displayed inside the version chip */
  versionLabel?: string;
};

const DEFAULT_SUBJECTS: SubjectOption[] = [
  { label: 'Astronomy', value: 'astronomy' },
  { label: 'Physics', value: 'physics' },
  { label: 'Biology', value: 'biology' },
  { label: 'Mathematics', value: 'mathematics' },
];

const prefersDarkMode = () =>
  typeof window !== 'undefined' &&
  window.matchMedia &&
  window.matchMedia('(prefers-color-scheme: dark)').matches;

export default function Header({
  logoText = 'Super Encyclopedia',
  subjects = DEFAULT_SUBJECTS,
  selectedSubject,
  onSubjectChange,
  onSearch,
  versionLabel = 'v0.1',
}: HeaderProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [theme, setTheme] = useState<'light' | 'dark'>(() =>
    prefersDarkMode() ? 'dark' : 'light',
  );

  const subjectValue = useMemo(() => {
    if (selectedSubject) return selectedSubject;
    return subjects[0]?.value ?? '';
  }, [selectedSubject, subjects]);

  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.documentElement.dataset.theme = theme;
    }
  }, [theme]);

  const handleSubjectChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const nextValue = event.target.value;
    onSubjectChange?.(nextValue);
  };

  const handleSearchSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSearch?.(searchQuery.trim());
    if (!onSearch) {
      console.info('Search submitted (no backend wired yet):', searchQuery);
    }
  };

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <header style={styles.root}>
      <div style={styles.logoWrapper}>
        <a href="/" style={styles.logoLink} aria-label="Super Encyclopedia home">
          <span style={styles.logoGlyph} aria-hidden="true">
            🧭
          </span>
          <div>
            <strong style={styles.logoText}>{logoText}</strong>
            <p style={styles.logoSubtext}>Knowledge explorer</p>
          </div>
        </a>
        <span style={styles.versionChip}>{versionLabel}</span>
      </div>

      <div style={styles.controls}>
        <label style={styles.subjectLabel}>
          <span style={styles.labelText}>Subject</span>
          <select
            value={subjectValue}
            onChange={handleSubjectChange}
            style={styles.select}
            aria-label="Switch subject"
          >
            {subjects.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <form style={styles.searchForm} onSubmit={handleSearchSubmit} role="search">
          <label htmlFor="header-search" style={styles.srOnly}>
            Search encyclopedia
          </label>
          <input
            id="header-search"
            type="search"
            placeholder="Search for a concept"
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
            style={styles.searchInput}
          />
        </form>

        <button
          type="button"
          onClick={toggleTheme}
          style={styles.themeButton}
          aria-pressed={theme === 'dark'}
          aria-label={`Activate ${theme === 'dark' ? 'light' : 'dark'} mode`}
        >
          {theme === 'dark' ? '🌙 Dark' : '☀️ Light'}
        </button>
      </div>
    </header>
  );
}

const styles: Record<string, CSSProperties> = {
  root: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: '1rem',
    padding: '1rem 1.5rem',
    borderBottom: '1px solid rgba(0, 0, 0, 0.1)',
    background: 'var(--header-bg, #fff)',
    position: 'sticky',
    top: 0,
    zIndex: 10,
  },
  logoWrapper: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  logoLink: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.75rem',
    textDecoration: 'none',
    color: 'inherit',
  },
  logoGlyph: {
    fontSize: '1.75rem',
    lineHeight: 1,
  },
  logoText: {
    fontSize: '1.1rem',
  },
  logoSubtext: {
    margin: 0,
    fontSize: '0.85rem',
    color: 'var(--muted-text, #666)',
  },
  versionChip: {
    fontSize: '0.75rem',
    background: 'var(--chip-bg, #eef2ff)',
    color: 'var(--chip-text, #4c1d95)',
    borderRadius: '999px',
    padding: '0.2rem 0.65rem',
    fontWeight: 600,
  },
  controls: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    marginLeft: 'auto',
  },
  subjectLabel: {
    display: 'flex',
    flexDirection: 'column',
    fontSize: '0.75rem',
    fontWeight: 600,
    color: 'var(--muted-text, #555)',
  },
  labelText: {
    marginBottom: '0.2rem',
  },
  select: {
    padding: '0.4rem 0.6rem',
    borderRadius: '0.5rem',
    border: '1px solid rgba(0, 0, 0, 0.15)',
    minWidth: '8rem',
  },
  searchForm: {
    flex: 1,
    minWidth: '12rem',
  },
  searchInput: {
    width: '100%',
    padding: '0.45rem 0.8rem',
    borderRadius: '999px',
    border: '1px solid rgba(0, 0, 0, 0.15)',
    fontSize: '0.9rem',
  },
  themeButton: {
    border: '1px solid rgba(0, 0, 0, 0.2)',
    background: 'transparent',
    borderRadius: '999px',
    padding: '0.35rem 0.9rem',
    cursor: 'pointer',
  },
  srOnly: {
    position: 'absolute',
    width: '1px',
    height: '1px',
    padding: 0,
    margin: '-1px',
    overflow: 'hidden',
    clip: 'rect(0, 0, 0, 0)',
    border: 0,
  },
};
