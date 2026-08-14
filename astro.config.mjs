import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

// Deploy target: GitHub Pages, project site at prime-radiant-inc/shipped
// -> served from https://prime-radiant-inc.github.io/shipped/
//
// If this ever moves to a custom domain (e.g. via a CNAME file in public/),
// change `base` to '/' and update `site` to the custom domain. Project-page
// GitHub Pages sites are served under a /<repo-name>/ path unless a custom
// domain is configured, so `base` MUST match the repo name until then.
export default defineConfig({
  site: 'https://prime-radiant-inc.github.io',
  base: '/shipped',
  integrations: [mdx()],
});
