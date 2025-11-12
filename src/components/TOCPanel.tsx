import type { CSSProperties } from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

type HeadingLevel = 2 | 3;

type HeadingEntry = {
  id: string;
  text: string;
  level: HeadingLevel;
};

export interface TOCPanelProps {
  /**
   * CSS selector that resolves to the container that wraps the rendered Markdown.
   * Defaults to the first <article> element on the page.
   */
  articleSelector?: string;
  /**
   * Selector that determines which headings are collected.
   * By default we watch <h2> and <h3> elements.
   */
  headingSelector?: string;
  /**
   * Optional additional CSS class applied to the root element.
   */
  className?: string;
  /**
   * Offset used when determining which heading is "active".
   * Helpful when the layout uses a fixed header.
   */
  scrollOffset?: number;
}

const slugify = (value: string) =>
  value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-');

const focusableSelectors = ['input', 'textarea', 'select'];

const getHeadingLevel = (tagName: string): HeadingLevel | null => {
  if (tagName.toLowerCase() === 'h2') return 2;
  if (tagName.toLowerCase() === 'h3') return 3;
  return null;
};

const ensureUniqueId = (baseId: string, occupied: Set<string>) => {
  let id = baseId || 'section';
  let suffix = 2;
  while (occupied.has(id)) {
    id = `${baseId}-${suffix++}`;
  }
  occupied.add(id);
  return id;
};

const buildHeadingList = (container: Element, selector: string): HeadingEntry[] => {
  const occupied = new Set<string>();
  return Array.from(container.querySelectorAll<HTMLElement>(selector))
    .map((heading, index) => {
      const level = getHeadingLevel(heading.tagName);
      if (!level) return null;

      if (!heading.id) {
        const baseId = slugify(heading.textContent || `section-${index + 1}`);
        heading.id = ensureUniqueId(baseId, occupied);
      } else {
        heading.id = ensureUniqueId(heading.id, occupied);
      }

      return {
        id: heading.id,
        text: heading.textContent?.trim() || `Section ${index + 1}`,
        level,
      } satisfies HeadingEntry;
    })
    .filter((entry): entry is HeadingEntry => Boolean(entry));
};

const shouldIgnoreKey = (event: KeyboardEvent) => {
  const target = event.target as HTMLElement | null;
  if (!target) return false;
  const tagName = target.tagName.toLowerCase();
  if (focusableSelectors.includes(tagName)) return true;
  if (target.getAttribute('contenteditable') === 'true') return true;
  return false;
};

const TOCPanel = ({
  articleSelector = 'article',
  headingSelector = 'h2, h3',
  className,
  scrollOffset = 120,
}: TOCPanelProps) => {
  const [headings, setHeadings] = useState<HeadingEntry[]>([]);
  const [activeId, setActiveId] = useState<string>('');
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const article = document.querySelector(articleSelector);
    if (!article) {
      setHeadings([]);
      return;
    }
    setHeadings(buildHeadingList(article, headingSelector));
  }, [articleSelector, headingSelector]);

  useEffect(() => {
    if (!headings.length) return;

    const handleScroll = () => {
      const scrollPosition = window.scrollY + scrollOffset;
      let current = headings[0]?.id ?? '';

      for (const heading of headings) {
        const element = document.getElementById(heading.id);
        if (!element) continue;
        const elementOffset = element.getBoundingClientRect().top + window.scrollY;
        if (elementOffset - 2 <= scrollPosition) {
          current = heading.id;
        } else {
          break;
        }
      }

      setActiveId(current);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, [headings, scrollOffset]);

  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if (event.key !== '/' || event.metaKey || event.ctrlKey || event.altKey) return;
      if (shouldIgnoreKey(event)) return;
      event.preventDefault();
      inputRef.current?.focus();
    };

    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  const filteredHeadings = useMemo(() => {
    if (!query.trim()) return headings;
    const normalized = query.trim().toLowerCase();
    return headings.filter((heading) => heading.text.toLowerCase().includes(normalized));
  }, [headings, query]);

  const handleNavigate = useCallback((headingId: string) => {
    const headingElement = document.getElementById(headingId);
    if (!headingElement) return;
    headingElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    history.replaceState(null, '', `#${headingId}`);
  }, []);

  const baseClass = ['toc-panel', className].filter(Boolean).join(' ');

  return (
    <aside className={baseClass} style={styles.container} aria-label="Table of contents">
      <div style={styles.header}>
        <div style={styles.titleRow}>
          <span style={styles.title}>On this page</span>
          <kbd style={styles.shortcut}>/</kbd>
        </div>
        <label style={styles.searchLabel} aria-label="Filter sections">
          <input
            ref={inputRef}
            type="search"
            placeholder="Filter sections"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            style={styles.input}
          />
        </label>
      </div>
      <nav style={styles.listWrapper}>
        {filteredHeadings.length === 0 && (
          <p style={styles.emptyState}>No matching sections.</p>
        )}
        <ol style={styles.list}>
          {filteredHeadings.map((heading) => {
            const isActive = heading.id === activeId;
            return (
              <li key={heading.id} style={{ ...styles.listItem, marginLeft: heading.level === 3 ? '1rem' : 0 }}>
                <a
                  href={`#${heading.id}`}
                  style={{
                    ...styles.link,
                    fontWeight: heading.level === 2 ? 600 : 500,
                    color: isActive ? '#0f172a' : '#475569',
                    backgroundColor: isActive ? 'rgba(59, 130, 246, 0.18)' : 'transparent',
                    borderLeft: isActive ? '3px solid #3b82f6' : '3px solid transparent',
                  }}
                  onClick={(event) => {
                    event.preventDefault();
                    handleNavigate(heading.id);
                  }}
                >
                  {heading.text}
                </a>
              </li>
            );
          })}
        </ol>
      </nav>
    </aside>
  );
};

const styles: Record<string, CSSProperties> = {
  container: {
    position: 'sticky',
    top: '1.5rem',
    border: '1px solid #e2e8f0',
    borderRadius: '0.75rem',
    padding: '1rem',
    maxHeight: 'calc(100vh - 3rem)',
    overflowY: 'auto',
    backgroundColor: '#ffffff',
    boxShadow: '0 1px 2px rgba(15, 23, 42, 0.08)',
  },
  header: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
    marginBottom: '1rem',
  },
  titleRow: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: '0.75rem',
  },
  title: {
    fontSize: '0.95rem',
    fontWeight: 600,
    color: '#0f172a',
  },
  shortcut: {
    backgroundColor: '#f1f5f9',
    border: '1px solid #cbd5f5',
    borderRadius: '0.35rem',
    fontFamily: 'inherit',
    fontSize: '0.75rem',
    padding: '0.15rem 0.35rem',
    color: '#475569',
  },
  searchLabel: {
    width: '100%',
  },
  input: {
    width: '100%',
    borderRadius: '0.5rem',
    border: '1px solid #cbd5f5',
    padding: '0.35rem 0.5rem',
    fontSize: '0.9rem',
  },
  listWrapper: {
    margin: 0,
    padding: 0,
  },
  list: {
    listStyle: 'none',
    margin: 0,
    padding: 0,
    display: 'flex',
    flexDirection: 'column',
    gap: '0.25rem',
  },
  listItem: {
    margin: 0,
  },
  link: {
    display: 'block',
    padding: '0.35rem 0.5rem',
    borderRadius: '0.5rem',
    textDecoration: 'none',
    transition: 'background-color 0.15s ease, color 0.15s ease',
  },
  emptyState: {
    margin: '0 0 0.75rem',
    color: '#94a3b8',
    fontSize: '0.85rem',
  },
};

export default TOCPanel;
