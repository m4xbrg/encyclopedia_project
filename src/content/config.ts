import { defineCollection, z } from 'astro:content';
import { CONCEPT_TAGS, COURSE_TAGS, LESSON_TAGS, SUBJECT_SLUGS } from '../data/taxonomy';

const enumFromValues = <T extends readonly [string, ...string[]]>(values: T) => z.enum(values);

const tagListSchema = <T extends readonly [string, ...string[]]>(values: T, description: string) =>
  z
    .array(enumFromValues(values))
    .default([])
    .describe(description);

const courseTagSchema = tagListSchema(
  COURSE_TAGS,
  'Discovery tags for courses defined in src/data/taxonomy.ts'
);

const lessonTagSchema = tagListSchema(
  LESSON_TAGS,
  'Discovery tags for lessons defined in src/data/taxonomy.ts'
);

const conceptTagSchema = tagListSchema(
  CONCEPT_TAGS,
  'Discovery tags for concepts defined in src/data/taxonomy.ts'
);

const courses = defineCollection({
  type: 'content',
  schema: ({ slug }) =>
    z
      .object({
        code: z.string().describe('Short identifier for the course'),
        title: z.string().describe('Human readable course name'),
        description: z.string().describe('Overview of the course'),
        level: z.string().optional().describe('Target experience level'),
        tags: courseTagSchema,
      })
      .refine((data) => data.code.toLowerCase() === slug.toLowerCase(), {
        message: 'The course code must match the file slug',
        path: ['code'],
      }),
});

const lessons = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    courseCode: z.string().describe('Slug of the course this lesson belongs to'),
    order: z.number().int().nonnegative().optional(),
    tags: lessonTagSchema,
  }),
});

const concepts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    subject: enumFromValues(SUBJECT_SLUGS).describe(
      'Slug of the subject defined in src/data/taxonomy.ts'
    ),
    tags: conceptTagSchema,
  }),
});

export const collections = { courses, lessons, concepts };
