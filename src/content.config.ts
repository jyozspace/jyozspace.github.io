import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Blog posts — write these as plain Markdown files in src/content/blog/*.md
const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    date: z.date(),
    excerpt: z.string(),
    category: z.string().default('General'),
    draft: z.boolean().default(false),
  }),
});

// Project entries shown on /projects — one Markdown file per project.
// The Markdown body (if any) is not currently rendered on the list page,
// but is available for a future per-project detail page.
const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    status: z.enum(['startup', 'ongoing', 'completed', 'on-hold', 'commercialisation']),
    affiliation: z.string(),
    task: z.string(),
    link: z.string().url().optional(),
    order: z.number().default(0),
    // Major/professional projects render as full cards on /projects; everything
    // else (RoboTech-club-era tinkering) collapses into the "hobby projects" list.
    featured: z.boolean().default(false),
  }),
});

// Research publications shown on /research — one Markdown file per paper.
// The Markdown body is the abstract.
const publications = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/publications' }),
  schema: z.object({
    title: z.string(),
    authors: z.string(),
    venue: z.string(),
    doi: z.string().url().optional(),
    doiLabel: z.string().optional(),
    arxiv: z.string().url().optional(),
    image: z.string().optional(),
    order: z.number().default(0),
  }),
});

export const collections = { blog, projects, publications };
