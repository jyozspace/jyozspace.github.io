import { defineConfig } from 'astro/config';

// Site is served from the custom domain (see /public/CNAME), so it lives at
// the domain root rather than a /repo-name/ subpath.
export default defineConfig({
  site: 'https://jyozspace.in',
});
