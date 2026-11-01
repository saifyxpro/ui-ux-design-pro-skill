import { create, insertMultiple, search as oramaSearch } from '@orama/orama';
import { stemmer } from '@orama/stemmers/english';
import { readdir, readFile } from 'fs/promises';
import { join } from 'path';
import chalk from 'chalk';
import { parseCsv } from './csv';

// Define the "Masterpiece" Schema
// We map all distinct CSVs into this unified structure for global search
type DesignDoc = {
  id: string;
  category: string; // The filename, or 'stack:<name>' for data/stacks/ (e.g., 'styles', 'stack:nextjs')
  source: string;   // Same value as category, as an enum so that filters match it exactly
  title: string;    // The primary name/key
  content: string;  // The full searchable text
  raw: string;      // Original data as JSON string for display
};

const DATA_DIR = join(import.meta.dir, '../data');
const STACKS_DIR = join(DATA_DIR, 'stacks');

// Map CSV filenames to their "primary key" column for the title
const TITLE_KEYS: Record<string, string[]> = {
  'styles.csv': ['Style Category', 'Style', 'Name'],
  'colors.csv': ['Industry', 'Palette'],
  'icons.csv': ['Icon Name'],
  'icon-libraries.csv': ['name'],
  'ui-reasoning.csv': ['Category', 'Pattern'],
  'ux-guidelines.csv': ['Issue', 'Category'],
  'typography.csv': ['Pairing', 'Font'],
  'ai-hallucinations.csv': ['Error_Name', 'Category'],
  'components.csv': ['Name', 'Category'],
};

// Public --domain names, each mapped to the category of its CSV file in data/
export const DOMAINS: Record<string, string> = {
  product: 'products',
  style: 'styles',
  typography: 'typography',
  color: 'colors',
  landing: 'landing',
  chart: 'charts',
  ux: 'ux-guidelines',
  reasoning: 'ui-reasoning',
  react: 'react-performance',
  web: 'web-interface',
  icon: 'icons',
  'icon-library': 'icon-libraries',
  component: 'components',
  hallucination: 'ai-hallucinations',
};

// Stack names are the file names in data/stacks/ (e.g. 'nextjs', 'react-native')
async function listStacks(): Promise<string[]> {
  const files = await readdir(STACKS_DIR);
  return files.filter(f => f.endsWith('.csv')).map(f => f.replace('.csv', '')).sort();
}

// Global index singleton
let db: any = null;

export async function getIndex() {
  if (db) return db;

  // Initialize Orama
  db = await create({
    schema: {
      id: 'string',
      category: 'string',
      source: 'enum',
      title: 'string',
      content: 'string',
      raw: 'string',
    },
    components: {
      tokenizer: {
        stemming: true,
        stemmer,
      },
    },
  });

  // Load all CSVs
  try {
    const files = await readdir(DATA_DIR);
    const csvFiles = files.filter(f => f.endsWith('.csv'));
    const sources = [
      ...csvFiles.map(file => ({
        file,
        filePath: join(DATA_DIR, file),
        category: file.replace('.csv', ''),
        titleKeys: TITLE_KEYS[file],
      })),
      ...(await listStacks()).map(stack => ({
        file: `stacks/${stack}.csv`,
        filePath: join(STACKS_DIR, `${stack}.csv`),
        category: `stack:${stack}`,
        titleKeys: ['Guideline'],
      })),
    ];

    // console.log(chalk.gray(`Indexing ${sources.length} databases...`));

    const docs: DesignDoc[] = [];

    for (const { file, filePath, category, titleKeys } of sources) {
      const csvContent = await readFile(filePath, 'utf-8');

      try {
        const records = parseCsv(csvContent);

        for (const [index, row] of records.entries()) {
          // Find a suitable title
          let title = 'Unknown';
          const possibleKeys = titleKeys || Object.keys(row as object);
          for (const key of possibleKeys) {
            if ((row as Record<string, string>)[key]) {
              title = (row as Record<string, string>)[key] || 'Unknown';
              break;
            }
          }

          // Create a rich content string for searching
          // Filter out negative columns to avoid "Do Not Use For: Healthcare" matching "Healthcare" query
          const negativeKeys = ['Do Not Use For', 'Don\'t', 'Code Example Bad', 'Code Bad'];
          
          const content = Object.entries(row as object)
            .filter(([key]) => !negativeKeys.some(neg => key.includes(neg)))
            .map(([_, val]) => val)
            .join(' ');

          docs.push({
            id: `${category}-${index}`,
            category,
            source: category,
            title,
            content,
            raw: JSON.stringify(row),
          });
        }
      } catch (parseErr) {
        console.warn(chalk.yellow(`Warning: Failed to parse ${file}:`), parseErr instanceof Error ? parseErr.message : parseErr);
      }
    }

    await insertMultiple(db, docs);
    return db;

  } catch (err) {
    console.error(chalk.red('Failed to index data:'), err);
    return db;
  }
}

type SearchFilter = { domain?: string; stack?: string };

async function resolveSource({ domain, stack }: SearchFilter): Promise<string | undefined> {
  if (domain !== undefined && stack !== undefined) throw new Error('Use either a domain or a stack, not both');

  if (domain !== undefined) {
    const category = Object.hasOwn(DOMAINS, domain) ? DOMAINS[domain] : undefined;
    if (!category) throw new Error(`Unknown domain "${domain}". Available domains: ${Object.keys(DOMAINS).join(', ')}`);
    return category;
  }

  if (stack !== undefined) {
    const stacks = await listStacks();
    if (!stacks.includes(stack)) throw new Error(`Unknown stack "${stack}". Available stacks: ${stacks.join(', ')}`);
    return `stack:${stack}`;
  }
}

export async function searchDesign(query: string, filter: SearchFilter = {}) {
  const source = await resolveSource(filter);
  const index = await getIndex();
  
  const results = await oramaSearch(index, {
    term: query,
    properties: '*', // Search all fields
    threshold: 0.2, // Fuzzy tolerance
    tolerance: 1,
    limit: 20,
    where: source ? { source: { eq: source } } : undefined,
    boost: {
      title: 2,
      category: 1.5,
      content: 1,
    },
  });

  return results.hits.map(hit => ({
    id: hit.document.id,
    score: hit.score,
    category: hit.document.category,
    title: hit.document.title,
    data: JSON.parse(hit.document.raw as string),
  }));
}
