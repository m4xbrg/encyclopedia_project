import { defineCollection, z } from 'astro:content';

const courses = defineCollection({
  type: 'content',
  schema: ({ slug }) =>
    z
      .object({
        code: z.string().describe('Short identifier for the course'),
        title: z.string().describe('Human readable course name'),
        description: z.string().describe('Overview of the course'),
        level: z.string().optional().describe('Target experience level'),
        tags: z
          .array(z.string())
          .optional()
          .describe('Optional tags that help group courses'),
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
    tags: z
      .array(z.string())
      .optional()
      .describe('Optional tags to organize lessons'),
  }),
});

const concepts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    subject: z
      .string()
      .regex(/^[a-z0-9-]+$/, 'Subject must be a URL friendly slug'),
    tags: z
      .array(z.string())
      .optional()
      .describe('Optional tags describing the concept'),
  }),
});

export const collections = { courses, lessons, concepts };
