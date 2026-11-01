import { parse } from 'csv-parse/sync';

// Strict on purpose: a malformed row must throw instead of being merged or shifted silently.
export function parseCsv(content: string): Record<string, string>[] {
  return parse(content, {
    columns: true,
    skip_empty_lines: true,
    trim: true,
  });
}
