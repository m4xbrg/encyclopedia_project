/**
 * Taxonomy constants shared between the Astro content collections and UI.
 *
 * Centralising these values keeps the content schemas in sync with the
 * discovery filters used by the site.
 */
export type NonEmptyStringArray = readonly [string, ...string[]];

export const SUBJECT_SLUGS = [
  'astronomy',
  'astrophysics',
  'spaceflight',
  'mathematics',
  'history-of-science',
] as const satisfies NonEmptyStringArray;

export const SUBJECT_METADATA: Record<
  (typeof SUBJECT_SLUGS)[number],
  { title: string; description: string }
> = {
  astronomy: {
    title: 'Astronomy',
    description:
      'Study of celestial objects, their motions, and the stories they tell about the universe.',
  },
  astrophysics: {
    title: 'Astrophysics',
    description: 'Physics applied to phenomena such as stars, galaxies, and cosmology.',
  },
  spaceflight: {
    title: 'Spaceflight',
    description: 'Human and robotic exploration, vehicles, and mission operations beyond Earth.',
  },
  mathematics: {
    title: 'Mathematics',
    description: 'Foundational tools for reasoning, modelling, and quantitative problem solving.',
  },
  'history-of-science': {
    title: 'History of Science',
    description: 'Context for major discoveries, cultures of research, and scientific biographies.',
  },
};

export const COURSE_TAGS = [
  'observational-skills',
  'math-foundations',
  'project-based',
  'history-rich',
  'instrumentation',
] as const satisfies NonEmptyStringArray;

export const LESSON_TAGS = [
  'activity',
  'demonstration',
  'reading',
  'lab',
  'assessment',
] as const satisfies NonEmptyStringArray;

export const CONCEPT_TAGS = [
  'definition',
  'phenomenon',
  'equipment',
  'technique',
  'historical-note',
] as const satisfies NonEmptyStringArray;

export const TAG_DESCRIPTIONS: Record<
  (typeof COURSE_TAGS)[number] | (typeof LESSON_TAGS)[number] | (typeof CONCEPT_TAGS)[number],
  string
> = {
  'observational-skills': 'Guidance on reading the night sky and documenting observations.',
  'math-foundations': 'Coursework rooted in quantitative reasoning or proofs.',
  'project-based': 'Learners complete multi-step or collaborative projects.',
  'history-rich': 'Explores the cultural or historical context of discoveries.',
  instrumentation: 'Focus on telescopes, detectors, and other tools of the trade.',
  activity: 'Hands-on work that asks learners to apply a concept immediately.',
  demonstration: 'Instructor-led walkthroughs that model the target skill.',
  reading: 'Primary or secondary source readings that extend the lesson.',
  lab: 'Structured experiments or investigations.',
  assessment: 'Checks for understanding, rubrics, or study guides.',
  definition: 'A precise description of an idea, object, or process.',
  phenomenon: 'Natural events and patterns worth observing and explaining.',
  equipment: 'Tools, instruments, or materials needed for a task.',
  technique: 'Repeatable procedure or method.',
  'historical-note': 'Biographical or contextual background information.',
};

export const TAXONOMY = {
  subjects: SUBJECT_SLUGS,
  tags: {
    course: COURSE_TAGS,
    lesson: LESSON_TAGS,
    concept: CONCEPT_TAGS,
  },
} as const;
