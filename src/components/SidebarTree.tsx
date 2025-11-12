import type { KeyboardEvent } from 'react';
import { useEffect, useMemo, useRef, useState } from 'react';

export type SidebarTreeItem = {
  id: string;
  label: string;
  href?: string;
  children?: SidebarTreeItem[];
};

export type SidebarTreeProps = {
  /** Tree structure to render. */
  items: SidebarTreeItem[];
  /** Link that should be marked as active. */
  activeHref?: string;
  /** Nodes that should be expanded on first render. */
  defaultExpandedIds?: string[];
  /** Optional class name for the outer <ul>. */
  className?: string;
};

type VisibleItem = {
  id: string;
  level: number;
  parentId: string | null;
  hasChildren: boolean;
  isExpanded: boolean;
  item: SidebarTreeItem;
};

const normalizeHref = (href?: string) => (href ? href.replace(/\/+$/, '').toLowerCase() : '');

const buildNodeMap = (
  nodes: SidebarTreeItem[],
  map: Map<string, SidebarTreeItem> = new Map(),
): Map<string, SidebarTreeItem> => {
  for (const node of nodes) {
    map.set(node.id, node);
    if (node.children?.length) {
      buildNodeMap(node.children, map);
    }
  }

  return map;
};

const buildParentMap = (
  nodes: SidebarTreeItem[],
  parentId: string | null = null,
  map: Record<string, string | null> = {},
): Record<string, string | null> => {
  for (const node of nodes) {
    map[node.id] = parentId;
    if (node.children?.length) {
      buildParentMap(node.children, node.id, map);
    }
  }

  return map;
};

const findPathToHref = (
  nodes: SidebarTreeItem[],
  targetHref: string,
  currentPath: string[] = [],
): string[] | null => {
  for (const node of nodes) {
    const nextPath = [...currentPath, node.id];
    if (normalizeHref(node.href) === targetHref) {
      return nextPath;
    }

    if (node.children?.length) {
      const result = findPathToHref(node.children, targetHref, nextPath);
      if (result) {
        return result;
      }
    }
  }

  return null;
};

const collectVisibleItems = (
  nodes: SidebarTreeItem[],
  expanded: Record<string, boolean>,
  level = 1,
  parentId: string | null = null,
): VisibleItem[] => {
  const visible: VisibleItem[] = [];

  for (const node of nodes) {
    const hasChildren = Boolean(node.children?.length);
    const isExpanded = Boolean(expanded[node.id]);

    visible.push({ id: node.id, level, parentId, hasChildren, isExpanded, item: node });

    if (hasChildren && isExpanded) {
      visible.push(...collectVisibleItems(node.children ?? [], expanded, level + 1, node.id));
    }
  }

  return visible;
};

const SidebarTree = ({
  items,
  activeHref,
  defaultExpandedIds = [],
  className,
}: SidebarTreeProps) => {
  const normalizedActiveHref = normalizeHref(activeHref);
  const nodeMap = useMemo(() => buildNodeMap(items), [items]);
  const activePath = useMemo(
    () => (normalizedActiveHref ? findPathToHref(items, normalizedActiveHref) : null),
    [items, normalizedActiveHref],
  );
  const parentMap = useMemo(() => buildParentMap(items), [items]);

  const [expanded, setExpanded] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    const idsToExpand = new Set(defaultExpandedIds);

    if (activePath) {
      activePath.forEach((nodeId, index) => {
        const node = nodeMap.get(nodeId);
        const hasChildren = Boolean(node?.children?.length);
        if (index < activePath.length - 1 || hasChildren) {
          idsToExpand.add(nodeId);
        }
      });
    }

    idsToExpand.forEach((nodeId) => {
      initial[nodeId] = true;
    });

    return initial;
  });

  const [focusedId, setFocusedId] = useState<string | null>(() => {
    if (activePath?.length) {
      return activePath[activePath.length - 1];
    }
    return items[0]?.id ?? null;
  });

  const visibleItems = useMemo(() => collectVisibleItems(items, expanded), [items, expanded]);
  const visibleIds = useMemo(() => visibleItems.map((item) => item.id), [visibleItems]);
  const visibleMap = useMemo(() => {
    const map: Record<string, VisibleItem> = {};
    visibleItems.forEach((item) => {
      map[item.id] = item;
    });
    return map;
  }, [visibleItems]);

  const itemRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const linkRefs = useRef<Record<string, HTMLAnchorElement | null>>({});

  useEffect(() => {
    if (!focusedId) {
      if (visibleIds.length) {
        setFocusedId(visibleIds[0]);
      }
      return;
    }

    if (!visibleIds.includes(focusedId)) {
      const parentId = parentMap[focusedId];
      if (parentId && visibleIds.includes(parentId)) {
        setFocusedId(parentId);
      } else {
        setFocusedId(visibleIds[0] ?? null);
      }
    }
  }, [focusedId, visibleIds, parentMap]);

  useEffect(() => {
    if (focusedId) {
      const element = itemRefs.current[focusedId];
      element?.focus();
    }
  }, [focusedId]);

  const toggleNode = (nodeId: string) => {
    setExpanded((prev) => ({
      ...prev,
      [nodeId]: !prev[nodeId],
    }));
  };

  const moveFocusByOffset = (currentId: string, offset: number) => {
    const index = visibleIds.indexOf(currentId);
    if (index === -1) {
      return;
    }

    const nextId = visibleIds[index + offset];
    if (nextId) {
      setFocusedId(nextId);
    }
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>, nodeId: string) => {
    const metadata = visibleMap[nodeId];
    if (!metadata) {
      return;
    }

    switch (event.key) {
      case 'ArrowDown': {
        event.preventDefault();
        moveFocusByOffset(nodeId, 1);
        break;
      }
      case 'ArrowUp': {
        event.preventDefault();
        moveFocusByOffset(nodeId, -1);
        break;
      }
      case 'ArrowRight': {
        if (!metadata.hasChildren) {
          break;
        }
        event.preventDefault();
        if (!metadata.isExpanded) {
          toggleNode(nodeId);
        } else {
          const firstChildId = metadata.item.children?.[0]?.id;
          if (firstChildId) {
            setFocusedId(firstChildId);
          }
        }
        break;
      }
      case 'ArrowLeft': {
        event.preventDefault();
        if (metadata.hasChildren && metadata.isExpanded) {
          toggleNode(nodeId);
        } else if (metadata.parentId) {
          setFocusedId(metadata.parentId);
        }
        break;
      }
      case 'Home': {
        event.preventDefault();
        if (visibleIds.length) {
          setFocusedId(visibleIds[0]);
        }
        break;
      }
      case 'End': {
        event.preventDefault();
        if (visibleIds.length) {
          setFocusedId(visibleIds[visibleIds.length - 1]);
        }
        break;
      }
      case 'Enter':
      case ' ': {
        if (metadata.item.href) {
          event.preventDefault();
          linkRefs.current[metadata.id]?.click();
        } else if (metadata.hasChildren) {
          event.preventDefault();
          toggleNode(metadata.id);
        }
        break;
      }
      default:
        break;
    }
  };

  const renderNodes = (nodes: SidebarTreeItem[], level = 1): JSX.Element | null => {
    if (!nodes.length) {
      return null;
    }

    const role = level === 1 ? 'tree' : 'group';

    return (
      <ul role={role} className={level === 1 ? className : undefined}>
        {nodes.map((node) => {
          const hasChildren = Boolean(node.children?.length);
          const isExpanded = Boolean(expanded[node.id]);
          const isActive = Boolean(
            normalizedActiveHref && normalizeHref(node.href) === normalizedActiveHref,
          );
          const isFocused = focusedId === node.id;

          return (
            <li role="none" key={node.id}>
              <div
                role="treeitem"
                aria-level={level}
                aria-expanded={hasChildren ? isExpanded : undefined}
                tabIndex={isFocused ? 0 : -1}
                ref={(element) => {
                  itemRefs.current[node.id] = element;
                }}
                className={`sidebar-tree__item${isActive ? ' sidebar-tree__item--active' : ''}`}
                onKeyDown={(event) => handleKeyDown(event, node.id)}
                onFocus={() => setFocusedId(node.id)}
              >
                {hasChildren && (
                  <button
                    type="button"
                    className="sidebar-tree__toggle"
                    onClick={(event) => {
                      event.stopPropagation();
                      toggleNode(node.id);
                    }}
                    tabIndex={-1}
                    aria-hidden="true"
                  >
                    <span aria-hidden="true">{isExpanded ? '▾' : '▸'}</span>
                  </button>
                )}

                {node.href ? (
                  <a
                    href={node.href}
                    aria-current={isActive ? 'page' : undefined}
                    tabIndex={-1}
                    ref={(element) => {
                      linkRefs.current[node.id] = element;
                    }}
                    className="sidebar-tree__link"
                  >
                    {node.label}
                  </a>
                ) : (
                  <span className="sidebar-tree__label">{node.label}</span>
                )}
              </div>

              {hasChildren && isExpanded && node.children ? renderNodes(node.children, level + 1) : null}
            </li>
          );
        })}
      </ul>
    );
  };

  return renderNodes(items);
};

export default SidebarTree;
