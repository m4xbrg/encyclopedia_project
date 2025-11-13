export type TaxonomyTag = {
  slug: string;
  label: string;
  description: string;
};

export const domainTags: TaxonomyTag[] = [
  {
    slug: 'mathematics',
    label: 'Mathematics',
    description:
      'Pure and applied math topics ranging from algebra and geometry to analysis and probability.',
  },
  {
    slug: 'physical-sciences',
    label: 'Physical Sciences',
    description: 'Physics, astronomy, and chemistry foundations that describe the natural world.',
  },
  {
    slug: 'life-sciences',
    label: 'Life Sciences',
    description: 'Biology, ecology, and the study of complex living systems.',
  },
  {
    slug: 'computing-engineering',
    label: 'Computing & Engineering',
    description:
      'Computer science, data systems, and the engineering disciplines that apply scientific knowledge.',
  },
];

export const categoryTags: TaxonomyTag[] = [
  {
    slug: 'concepts',
    label: 'Concepts',
    description: 'Core ideas, definitions, and theoretical frameworks.',
  },
  {
    slug: 'methods',
    label: 'Methods',
    description: 'Procedural knowledge, laboratory techniques, and computational workflows.',
  },
  {
    slug: 'applications',
    label: 'Applications',
    description: 'Case studies, engineering designs, and real-world exemplars.',
  },
  {
    slug: 'history-context',
    label: 'History & Context',
    description: 'Narratives that place discoveries, people, and institutions in context.',
  },
];

export const thematicTags: TaxonomyTag[] = [
  {
    slug: 'systems-thinking',
    label: 'Systems Thinking',
    description: 'Highlights feedback loops, emergent behavior, and interconnected components.',
  },
  {
    slug: 'data-literacy',
    label: 'Data Literacy',
    description: 'Focuses on interpreting quantitative information and statistical reasoning.',
  },
  {
    slug: 'design-thinking',
    label: 'Design Thinking',
    description: 'Emphasizes empathy, prototyping, and iterative solution building.',
  },
  {
    slug: 'ethics-society',
    label: 'Ethics & Society',
    description: 'Explores the human impacts, policy implications, and equity concerns in a topic.',
  },
];

export const pedagogicalTags: TaxonomyTag[] = [
  {
    slug: 'inquiry-based',
    label: 'Inquiry-Based',
    description: 'Guides learners to pose questions, collect evidence, and build explanations.',
  },
  {
    slug: 'project-based',
    label: 'Project-Based',
    description: 'Centers on multi-step projects with milestones and deliverables.',
  },
  {
    slug: 'guided-practice',
    label: 'Guided Practice',
    description: 'Structured walkthroughs with scaffolding and worked examples.',
  },
  {
    slug: 'assessment-ready',
    label: 'Assessment Ready',
    description: 'Provides rubrics, checkpoints, or question banks for evaluation.',
  },
];

export const allTags = new Set<string>(
  [...domainTags, ...categoryTags, ...thematicTags, ...pedagogicalTags].map((tag) => tag.slug),
);
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
