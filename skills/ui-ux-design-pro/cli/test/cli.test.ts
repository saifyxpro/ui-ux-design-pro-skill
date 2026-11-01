import { describe, expect, test } from 'bun:test';
import { join } from 'path';

const CLI_DIR = join(import.meta.dir, '..');

function run(...args: string[]) {
  const { stdout, stderr, exitCode } = Bun.spawnSync(['bun', 'run', 'index.ts', ...args], { cwd: CLI_DIR });
  return { stdout: stdout.toString(), stderr: stderr.toString(), exitCode };
}

describe('search', () => {
  test('returns the same document ids from one run to the next', () => {
    const ids = () => JSON.parse(run('search', 'glassmorphism', '--format', 'json').stdout).map((hit: { id: string }) => hit.id);
    const first = ids();
    expect(first.length).toBeGreaterThan(0);
    expect(ids()).toEqual(first);
  });

  test('--stack limits results to that framework guide', () => {
    const hits = JSON.parse(run('search', 'useEffect', '--stack', 'react', '--format', 'json').stdout);
    expect(hits.length).toBeGreaterThan(0);
    expect(hits.every((hit: { category: string }) => hit.category === 'stack:react')).toBe(true);
  });

  test.each(['--domain', '--stack'])('an empty %s exits with an error', (flag) => {
    const { exitCode } = run('search', 'dashboard', flag, '');
    expect(exitCode).toBe(1);
  });

  test('an unknown domain exits with an error', () => {
    const { stderr, exitCode } = run('search', 'dashboard', '--domain', 'nope');
    expect(exitCode).toBe(1);
    expect(stderr).toContain('Unknown domain "nope"');
  });
});

describe('icons', () => {
  test('finds icons by name, with their import', () => {
    const { stdout } = run('icons', 'arrow');
    expect(stdout).toContain('## arrow-left');
    expect(stdout).toContain("import { ArrowLeft } from 'lucide-react'");
  });

  test('finds icons by keyword', () => {
    expect(run('icons', 'hamburger').stdout).toContain('## menu');
  });

  test('still finds icon libraries by name', () => {
    const { stdout } = run('icons', 'iconify');
    expect(stdout).toContain('## Iconify');
    expect(stdout).toContain('https://iconify.design');
  });

  test('a library name shows that library, not every icon it provides', () => {
    const { stdout } = run('icons', 'lucide');
    expect(stdout).toContain('## Lucide');
    expect(stdout).not.toContain('# Icons Matching');
  });

  test('says so when nothing matches', () => {
    expect(run('icons', 'zzzzzz').stdout).toContain('No icons or icon libraries found matching "zzzzzz"');
  });
});

describe('generate --stack', () => {
  test('json output carries the guidelines of that stack', () => {
    const system = JSON.parse(run('generate', 'dashboard', '--stack', 'nextjs', '--format', 'json').stdout);
    expect(system.stack_guidelines.length).toBeGreaterThan(0);
    expect(system.stack_guidelines.every((hit: { category: string }) => hit.category === 'stack:nextjs')).toBe(true);
  });

  // nuxt-ui and react-native have rows that only mention the word "high" without being high severity.
  test.each(['nextjs', 'nuxt-ui', 'react-native'])('%s falls back to high-severity guidelines when the query matches none of them', (stack) => {
    const system = JSON.parse(run('generate', 'zzzzzz', '--stack', stack, '--format', 'json').stdout);
    expect(system.stack_guidelines.length).toBeGreaterThan(0);
    expect(system.stack_guidelines.every((hit: { data: { Severity: string } }) => hit.data.Severity === 'High')).toBe(true);
  });

  test('markdown output has a section for the stack', () => {
    const { stdout } = run('generate', 'dashboard', '--stack', 'nextjs', '--format', 'markdown');
    expect(stdout).toContain('## 05. Stack Guidelines (nextjs)');
    expect(stdout).toContain('- **Do**:');
  });

  test('text output lists them', () => {
    const { stdout } = run('generate', 'component', '--stack', 'nextjs');
    expect(stdout).toContain('Stack guidelines (nextjs):');
    expect(stdout).toContain('Use Server Components by default');
  });

  test('without --stack there is no stack section', () => {
    const system = JSON.parse(run('generate', 'dashboard', '--format', 'json').stdout);
    expect(system.stack_guidelines).toBeUndefined();
  });

  test('an unknown stack exits with an error', () => {
    const { stderr, exitCode } = run('generate', 'dashboard', '--stack', 'html');
    expect(exitCode).toBe(1);
    expect(stderr).toContain('Unknown stack "html"');
    expect(stderr).toContain('html-tailwind');
  });
});
