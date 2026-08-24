import * as si from 'simple-icons';

// Not every tool below has a real brand mark available (Adobe's icons were
// pulled from simple-icons over trademark restrictions; SolidWorks, Altium,
// MAVLink, and PX4 were never added) — those render as plain text chips
// instead of a fabricated logo. See src/pages/index.astro's `skills` array.
type IconSlug = keyof typeof si;

export function getIcon(slug: string): { path: string; hex: string; title: string } | null {
  const key = ('si' + slug[0].toUpperCase() + slug.slice(1)) as IconSlug;
  const icon = si[key] as { path: string; hex: string; title: string } | undefined;
  return icon ? { path: icon.path, hex: icon.hex, title: icon.title } : null;
}
