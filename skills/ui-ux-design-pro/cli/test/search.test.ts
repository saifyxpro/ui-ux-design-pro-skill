import { describe, expect, test } from 'bun:test';
import { readdirSync } from 'fs';
import { join } from 'path';
import { DOMAINS, searchDesign } from '../lib/search';

describe('stack guides', () => {
  test('are part of a global search, titled by their guideline', async () => {
    const hits = await searchDesign('App Router');
    const hit = hits.find((h) => h.category === 'stack:nextjs');
    expect(hit?.title).toBe('Use App Router for new projects');
  });

  test('--stack keeps only that stack, not one sharing a prefix', async () => {
    const hits = await searchDesign('component', { stack: 'react' });
    expect(hits.length).toBeGreaterThan(0);
    expect(new Set(hits.map((h) => h.category))).toEqual(new Set(['stack:react']));
  });

  test('an unknown stack is an error naming the valid ones', async () => {
    await expect(searchDesign('component', { stack: 'html' })).rejects.toThrow(/Unknown stack "html".*html-tailwind/);
  });
});

describe('domains', () => {
  test.each([
    ['product', 'products'],
    ['style', 'styles'],
    ['typography', 'typography'],
    ['color', 'colors'],
    ['landing', 'landing'],
    ['chart', 'charts'],
    ['ux', 'ux-guidelines'],
    ['reasoning', 'ui-reasoning'],
    ['react', 'react-performance'],
    ['web', 'web-interface'],
    ['icon', 'icons'],
    ['icon-library', 'icon-libraries'],
    ['component', 'components'],
    ['hallucination', 'ai-hallucinations'],
  ])('%s searches only %s', async (domain, category) => {
    // An empty term matches every document in the domain, whatever its wording.
    const hits = await searchDesign('', { domain });
    expect(hits.length).toBeGreaterThan(0);
    expect(new Set(hits.map((h) => h.category))).toEqual(new Set([category]));
  });

  test('every database in data/ has a domain', () => {
    const databases = readdirSync(join(import.meta.dir, '../data'))
      .filter((file) => file.endsWith('.csv'))
      .map((file) => file.replace('.csv', ''));
    expect(Object.values(DOMAINS).sort()).toEqual(databases.sort());
  });

  test('an unknown domain is an error naming the valid ones', async () => {
    await expect(searchDesign('dashboard', { domain: 'styles' })).rejects.toThrow(/Unknown domain "styles".*style/);
  });

  test('domain and stack cannot be combined', async () => {
    await expect(searchDesign('dashboard', { domain: 'style', stack: 'react' })).rejects.toThrow(/either/);
  });
});
