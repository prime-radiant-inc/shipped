import { defineCollection, z } from 'astro:content';

// Weekly "Shipped" recap posts. One post per week bucket.
// Frontmatter fields per the brief:
//   title       - post title
//   week        - human label, e.g. "Week 32, 2026"
//   dateStart   - first day of the week bucket (YYYY-MM-DD)
//   dateEnd     - last day of the week bucket (YYYY-MM-DD)
//   pubDate     - when this post is/was published
//   summary     - one/two sentence teaser for the index page
//   draft       - true hides the post from the index (defaults to false)
const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    week: z.string(),
    dateStart: z.coerce.date(),
    dateEnd: z.coerce.date(),
    pubDate: z.coerce.date(),
    summary: z.string(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { posts };
