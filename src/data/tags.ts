export type Tag = {
  slug: string;
  label: string;
  description?: string;
};

export type TagCategory = {
  slug: string;
  title: string;
  description?: string;
  tags: Tag[];
};

export const tagCategories: TagCategory[] = [
  {
    slug: 'domain',
    title: 'Domain tags',
    description:
      'High-level disciplines used to organize the encyclopedia curriculum and LaTeX exports.',
    tags: [
      {
        slug: 'foundations-preliminaries',
        label: 'Foundations & Preliminaries',
        description: 'Logic, set theory, and the prerequisite toolkit shared by every learner.',
      },
      {
        slug: 'mathematical-logic-foundations-advanced',
        label: 'Mathematical Logic & Foundations (Advanced)',
        description: 'Graduate-level logic, proof theory, and computability topics.',
      },
      {
        slug: 'computer-science-fundamentals',
        label: 'Computer Science & Technology: Fundamentals',
        description: 'Algorithms, discrete math, and the theoretical underpinnings of CS.',
      },
      {
        slug: 'engineering-foundations',
        label: 'Engineering: Foundations of Engineering',
        description: 'Core physics, chemistry, and design principles applied to engineering contexts.',
      },
    ],
  },
  {
    slug: 'thematic',
    title: 'Thematic tags',
    description: 'Cross-cutting themes that highlight how learners engage with the material.',
    tags: [
      {
        slug: 'observation-skills',
        label: 'Observation Skills',
        description: 'Hands-on techniques for reading data, the sky, or experimental setups.',
      },
      {
        slug: 'computational-thinking',
        label: 'Computational Thinking',
        description: 'Abstraction, decomposition, and pattern matching for solving problems.',
      },
      {
        slug: 'instrumentation-tooling',
        label: 'Instrumentation & Tooling',
        description: 'Selecting, calibrating, and maintaining the tools required for study.',
      },
      {
        slug: 'modeling-simulation',
        label: 'Modeling & Simulation',
        description: 'Building mathematical and computational models to explain phenomena.',
      },
    ],
  },
  {
    slug: 'audience',
    title: 'Audience tags',
    description: 'Signals the level of experience or background knowledge assumed by an entry.',
    tags: [
      { slug: 'beginner', label: 'Beginner', description: 'No prior exposure required.' },
      {
        slug: 'intermediate',
        label: 'Intermediate',
        description: 'Assumes familiarity with core undergraduate material.',
      },
      {
        slug: 'advanced',
        label: 'Advanced',
        description: 'Targets readers who already work with graduate-level texts.',
      },
    ],
  },
  {
    slug: 'format',
    title: 'Format tags',
    description: 'Indicates how the content is delivered inside the encyclopedia.',
    tags: [
      {
        slug: 'reference-entry',
        label: 'Reference Entry',
        description: 'Definition-style writeups generated from the LaTeX prompt templates.',
      },
      {
        slug: 'guided-lesson',
        label: 'Guided Lesson',
        description: 'Step-by-step lessons that sit inside a larger course outline.',
      },
      {
        slug: 'lab-notebook',
        label: 'Lab Notebook',
        description: 'Practical explorations or experiment walk-throughs.',
      },
    ],
  },
];
