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
