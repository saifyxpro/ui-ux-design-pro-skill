import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { Glob } from 'bun';
import { join } from 'path';
import { parseCsv } from '../lib/csv';
import { searchDesign } from '../lib/search';

const DATA_DIR = join(import.meta.dir, '../data');
const csvFiles = [...new Glob('**/*.csv').scanSync(DATA_DIR)].sort();

describe('CSV databases', () => {
  test('databases are found', () => {
    expect(csvFiles.length).toBeGreaterThan(0);
  });

  describe.each(csvFiles)('%s', (file) => {
    const content = readFileSync(join(DATA_DIR, file), 'utf-8');

    test('uses LF line endings only', () => {
      expect(content.includes('\r')).toBe(false);
    });

    test('parses strictly, every row matching the header', () => {
      expect(() => parseCsv(content)).not.toThrow();
    });

    test('numbers rows in strictly increasing order when it has a No column', () => {
      const rows = parseCsv(content);
      if (!rows[0] || !('No' in rows[0])) return;
      const numbers = rows.map((row) => Number(row.No));
      expect(numbers.every((n, i) => Number.isInteger(n) && (i === 0 || n > numbers[i - 1]!))).toBe(true);
    });
  });

  // Mixed CRLF/LF line endings used to collapse rows 26-105 into a single record.
  test('charts.csv keeps all 105 chart types', () => {
    const rows = parseCsv(readFileSync(join(DATA_DIR, 'charts.csv'), 'utf-8'));
    expect(rows.length).toBe(105);
    expect(rows.at(-1)?.['Data Type']).toBe('Multi-head attention');
  });
});

describe('search index', () => {
  test('finds chart types from the end of charts.csv', async () => {
    const hits = await searchDesign('attention rollout', 'charts');
    expect(hits.map((hit) => hit.data['Data Type'])).toContain('Multi-head attention');
  });
});
