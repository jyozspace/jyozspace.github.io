# JyozSpace

Jyothish J. Kumar's personal portfolio site — static, built with [Astro](https://astro.build), deployed to GitHub Pages.

## Local development

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # outputs to dist/
npm run preview   # preview the production build locally
```

## Editing content

Almost everything editorial lives as plain Markdown with frontmatter — no need to touch component code for routine updates.

| What | Where |
|---|---|
| Blog posts | `src/content/blog/*.md` — add a new file, copy the frontmatter shape from an existing post |
| Projects | `src/content/projects/*.md` — `featured: true` puts it in the major-projects grid, `false`/omitted puts it in the collapsible hobby-projects list |
| Research publications | `src/content/publications/*.md` |
| Patents | inline array in `src/pages/research.astro` (small enough not to need its own collection) |
| Home/About/Research/Projects/Contact page text | `src/pages/*.astro` (the prose is inline JSX/HTML — safe to edit directly) |
| Personal/family content | `src/pages/about/personal.astro` (linked from the bottom of About, not in the main nav) |
| M.Sc. thesis semester timeline + demo video | `src/pages/research/msc-thesis-journey.astro` (linked from Research, not in the main nav) |
| Colors, fonts, spacing | `src/styles/global.css` (all design tokens are CSS variables at the top) |
| Nav links, social links | `src/components/Header.astro`, `src/components/Footer.astro`, `src/pages/contact.astro` |
| Resume/CV | `public/resume.pdf` — see below |

### Adding a blog post

Create `src/content/blog/my-post-slug.md`:

```md
---
title: "My post title"
date: 2026-08-20
category: "Projects"
excerpt: "One or two sentence summary shown on the blog listing page."
---

Post content in **Markdown** goes here.
```

The file name (minus `.md`) becomes the URL slug, e.g. `/blog/my-post-slug/`.

### Adding a project

Create `src/content/projects/my-project.md`:

```md
---
title: "Project name"
status: ongoing   # one of: startup | ongoing | completed | on-hold | commercialisation
affiliation: "Lab / club / company"
task: "Your role"
link: "https://example.com"   # optional
order: 10          # controls sort order within its group (lower = earlier)
featured: true     # true = shown as a full card in "Major projects"; false/omitted = collapsible hobby list
---

Optional longer description (only shown on featured cards' "Reference" flow today; kept for a future per-project page).
```

### Adding a publication

Create `src/content/publications/my-paper.md`:

```md
---
title: "Paper title"
authors: "You, Co-author"
venue: "Journal / conference name"
doi: "https://doi.org/..."     # optional
doiLabel: "10.xxxx/xxxx"       # optional, shown as link text
arxiv: "https://arxiv.org/..." # optional
order: 5
---

The abstract goes here as the Markdown body.
```

## Adding your resume

All three "Download resume" buttons (About, Projects, Research) link to `/resume.pdf`. Save your CV PDF as `public/resume.pdf` in this project (same filename, overwrite if it already exists) and it will be served at that URL automatically — no code changes needed. If the file isn't there yet, the buttons will 404 until you add it.

## Setting up the contact form

The Contact page ships with a form wired to [Formspree](https://formspree.io) (a free service that emails you form submissions — no backend needed for a static site).

1. Sign up free at https://formspree.io and create a new form.
2. Copy the form endpoint it gives you (looks like `https://formspree.io/f/abcdwxyz`).
3. Open `src/pages/contact.astro` and replace `YOUR_FORM_ID` in the `FORMSPREE_ENDPOINT` constant with your real id.

Until you do this, the form will render but submissions won't go anywhere.

## Deploying to GitHub Pages

1. Create a new **public** GitHub repository (any name — e.g. `portfolio`) and push this project to it:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```

2. On GitHub: go to the repo's **Settings → Pages**, and under "Build and deployment" set **Source** to **GitHub Actions**. The included workflow (`.github/workflows/deploy.yml`) will then build and deploy automatically on every push to `main`.

3. **Custom domain (jyozspace.in):** this repo already includes `public/CNAME` with `jyozspace.in` in it, so GitHub Pages will serve the site on your domain once DNS is pointed at it:
   - At your domain registrar/DNS provider, add these records (replacing any old ones that pointed at your WordPress host):
     - Four `A` records for the apex domain (`jyozspace.in`) pointing to GitHub Pages' IPs:
       `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
     - A `CNAME` record for `www` pointing to `<your-username>.github.io`
   - Back in **Settings → Pages**, enter `jyozspace.in` as the custom domain and enable **Enforce HTTPS** once it's available (can take up to 24h after DNS propagates).
   - DNS changes can take a few hours to propagate; until then the site will still be reachable at `https://<your-username>.github.io/<repo-name>/`.

## What changed from the old WordPress site

- Rebuilt as a static Astro site — no hosting/PHP/MySQL/plugins required, hosted free on GitHub Pages.
- Design refreshed to a warmer, more restrained "editorial" look for a more professional feel; the cartoon Bitmoji hero graphic and decorative Elementor background texture were dropped in favor of your actual photo and a cleaner layout.
- The 2 existing blog posts were migrated with only their excerpts (the old cache/RSS export didn't retain full post bodies) — see the note at the top of each post; fill in the rest whenever you get to it.
- The Contact page no longer lists a phone number or physical address (kept email + socials only); the old JS-rendered contact form was replaced with a Formspree-backed form (needs the one-time setup above).
- The full original WordPress export (`public_html.zip`, `content_extract/`) is kept in this folder locally for reference but is git-ignored — it is **not** part of the deployed site.

## What changed in the August 2026 content revamp

Repositioned around "chemistry graduate turned self-taught full-stack roboticist," using your latest CV (June 2026) as the source of truth:

- **Career timeline corrected**: MSc (NISER/HBNI, DAE) → UAV Systems Engineer, UAVIO Labs (under Dr. Arjun Jain) → Research Scholar, NISER (Swayansaasita/ADAS, Dec 2023–May 2025) → Project Associate, AHRC IIT Bhubaneswar (Jun 2025–present). IIT Kanpur summer internship added.
- **Affybo Systems** (your startup) is now featured on Home (a "Now building" banner) and as the top card on Projects, linking to affybo.com.
- **Projects page** split into "major projects" (Affybo, Railway Inspection, Swayansaasita, UAVIO, MIMA, MSc thesis, IIT Kanpur) shown as full cards, and a collapsible "DIY, tinkering & hobby projects" list for the earlier RoboTech Club builds.
- **Research page** now leads with Publications, adds a **Patents** section (both pending applications from your CV), and trims the MSc thesis section to a short summary + link to the [full thesis on NISER's repository](https://idr.niser.ac.in/jspui/handle/123456789/564) + a link to the semester-by-semester journey (moved to its own page, `/research/msc-thesis-journey/`).
- **About page** is now a professional Experience timeline + compact Education list + condensed leadership bullets. Family, hobbies, upbringing, and the Abdul Kalam inspiration section moved off the main page to `/about/personal/`, linked quietly at the bottom rather than shown by default.
- Skills sections (Home) rewritten to match your CV's Technical Skills, reframed with Chemistry as academic background rather than an active skill, since you now work exclusively in robotics.

## What changed in the theme swap (matched to affybo.com)

The site was re-themed from the original warm/editorial look to a modern indigo/purple gradient system matched to affybo.com's design language:

- **Design tokens** (colors, fonts) live in `src/styles/global.css` — the whole palette is CSS variables at the top, so re-theming again later is a token edit, not a rewrite. Typography is now all-sans (Inter, dropped the Fraunces serif).
- **`src/components/DarkHero.astro`** is the reusable dark-gradient-with-glow-orbs band used at the top of Home, About, Projects, Research, Contact, and Blog. It works by overriding `--text`, `--border`, `--accent`, etc. on itself — everything slotted inside (`.eyebrow`, `.btn`, `.lede`) picks up the dark-mode-appropriate colors automatically via normal CSS inheritance, no per-page overrides needed. Secondary pages (`/about/personal/`, `/research/msc-thesis-journey/`, 404) intentionally keep a plain light header, signaling they're a step removed from primary nav.
- **Buttons** (`.btn-primary`) are gradient-filled pills now; **cards** (`.card`) get a thin gradient accent bar along the top edge, cycling through 5 colors by position — no data changes needed, it's pure CSS `nth-of-type`.
- **`.text-gradient`** utility class applies the accent gradient to a word/phrase inline — used sparingly on one emphasis word per heading (never on personal names, to keep them legible).
- Tech icons (added in the content revamp) and the Affybo logo mark were unaffected by the re-theme — both already used token-driven colors.
