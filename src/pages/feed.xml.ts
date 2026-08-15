import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';

// Atom feed for the Shipped blog.
// Custom endpoint (rather than @astrojs/rss, which only emits RSS 2.0) so
// we can produce a spec-correct Atom 1.0 document.
// See: https://validator.w3.org/feed/docs/atom.html

function escapeXml(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

export async function GET(context: APIContext) {
  const allPosts = await getCollection('posts', ({ data }) => !data.draft);
  const posts = allPosts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  // context.site is the `site` from astro.config (no trailing slash guaranteed);
  // BASE_URL is the configured `base` (e.g. "/shipped"). Combine for canonical URLs.
  const siteUrl = new URL(import.meta.env.BASE_URL, context.site);
  const base = siteUrl.toString().replace(/\/$/, '');

  const feedUrl = `${base}/feed.xml`;
  const postUrl = (slug: string) => `${base}/posts/${slug}`;

  const updated = (posts[0]?.data.pubDate ?? new Date()).toISOString();

  const entries = posts
    .map((post) => {
      const link = postUrl(post.slug);
      return `  <entry>
    <title>${escapeXml(post.data.title)}</title>
    <link href="${escapeXml(link)}" />
    <id>${escapeXml(link)}</id>
    <updated>${post.data.pubDate.toISOString()}</updated>
    <published>${post.data.pubDate.toISOString()}</published>
    <summary>${escapeXml(post.data.summary)}</summary>
  </entry>`;
    })
    .join('\n');

  const body = `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Shipped</title>
  <subtitle>A weekly recap of public-repo activity across prime-radiant-inc and obra.</subtitle>
  <link href="${escapeXml(feedUrl)}" rel="self" />
  <link href="${escapeXml(base + '/')}" />
  <id>${escapeXml(base + '/')}</id>
  <updated>${updated}</updated>
${entries}
</feed>
`;

  return new Response(body, {
    headers: { 'Content-Type': 'application/atom+xml; charset=utf-8' },
  });
}
