import { TAG_DESCRIPTIONS, TAXONOMY } from './taxonomy';

export type TagGroup = keyof typeof TAXONOMY.tags;
export type TagSlug = keyof typeof TAG_DESCRIPTIONS;

export type Tag = {
  slug: TagSlug;
  label: string;
  description?: string;
  href: string;
};

export type TagCategory = {
  slug: TagGroup;
  title: string;
  description: string;
  tags: Tag[];
};

export const TAG_GROUP_COPY: Record<TagGroup, { title: string; description: string }> = {
  course: {
    title: 'Course tags',
    description: 'Discovery signals that highlight how each course is structured and who it serves.',
  },
  lesson: {
    title: 'Lesson tags',
    description: 'Activity-focused markers that explain what learners do inside a lesson.',
  },
  concept: {
    title: 'Concept tags',
    description: 'Reference cues applied to encyclopedia entries that help readers scan the catalog.',
  },
};

export const formatTagLabel = (slug: string) =>
  slug
    .split('-')
    .filter(Boolean)
    .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
    .join(' ');

export const tagCategories: TagCategory[] = (
  Object.entries(TAXONOMY.tags) as [TagGroup, readonly TagSlug[]][]
).map(([group, tags]) => ({
  slug: group,
  title: TAG_GROUP_COPY[group].title,
  description: TAG_GROUP_COPY[group].description,
  tags: tags.map((tagSlug) => ({
    slug: tagSlug,
    label: formatTagLabel(tagSlug),
    description: TAG_DESCRIPTIONS[tagSlug],
    href: `/tags/${group}/${tagSlug}/`,
  })),
}));
