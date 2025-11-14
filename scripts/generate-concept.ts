#!/usr/bin/env ts-node
import { mkdirSync, existsSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const [, , titleArg, subjectArg, courseArg] = process.argv;

if (!titleArg || !subjectArg || !courseArg) {
  console.error('Usage: ts-node scripts/generate-concept.ts "<title>" "<subject>" "<course>"');
  process.exit(1);
}

const slugify = (value: string) =>
  value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-');

const title = titleArg.trim();
const subject = subjectArg.trim().toLowerCase();
const course = courseArg.trim();
const slug = slugify(title);

if (!slug) {
  console.error('Unable to create a slug from the provided title.');
  process.exit(1);
}

const conceptsDir = path.join('src', 'content', 'concepts', subject);
const outputPath = path.join(conceptsDir, `${slug}.mdx`);

if (existsSync(outputPath)) {
  console.error(`Concept file already exists: ${outputPath}`);
  process.exit(1);
}

mkdirSync(conceptsDir, { recursive: true });

const template = `---\ntitle: "${title}"\ndescription: ""\nsubject: "${subject}"\ncourse: "${course}"\ndifficulty: "intermediate"\nestimatedTime: ""\nlearningGoals:\n  - "TODO: Add the learning goals for this concept."\ntags:\n  - "TODO: Add relevant tags."\n---\n\nWrite the concept content here.\n`;

writeFileSync(outputPath, template, { encoding: 'utf-8' });

console.log(`Created concept: ${outputPath}`);
