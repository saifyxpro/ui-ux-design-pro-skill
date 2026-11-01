import { readFile } from 'fs/promises';
import { join } from 'path';
import chalk from 'chalk';
import { parseCsv } from '../lib/csv';
import { searchDesign } from '../lib/search';

const DATA_FILE = join(import.meta.dir, '../data/icon-libraries.csv');

type IconLibrary = {
  name: string;
  count: string;
  type: string;
  best_for: string;
  docs_url: string;
  cdn_url: string;
  implementation_type: string;
};

export async function iconsCommand(query?: string) {
  try {
    const csvContent = await readFile(DATA_FILE, 'utf-8');
    const records = parseCsv(csvContent) as IconLibrary[];

    if (query) {
      const libraries = records.filter((r) => 
        r.name.toLowerCase().includes(query.toLowerCase())
      );
      // The Library column is searchable too: a library name alone must not list its icons at random.
      const icons = (await searchDesign(query, { domain: 'icon' })).filter(({ data }) =>
        !data.Library.toLowerCase().includes(query.toLowerCase())
      );

      if (libraries.length === 0 && icons.length === 0) {
        console.log(chalk.yellow(`No icons or icon libraries found matching "${query}"`));
        return;
      }

      if (icons.length > 0) {
        console.log(`\n# Icons Matching "${query}"\n`);
        for (const { title, data } of icons) {
          console.log(`## ${title}`);
          console.log(`- **Library**: ${data.Library}`);
          console.log(`- **Import**: \`${data['Import Code']}\``);
          console.log(`- **Usage**: \`${data.Usage}\``);
          console.log(`- **Best For**: ${data['Best For']}`);
          console.log('');
        }
      }

      if (libraries.length > 0) {
        console.log(`\n# Icon Libraries Matching "${query}"\n`);
        for (const r of libraries) {
          console.log(`## ${r.name}`);
          console.log(`- **Count**: ${r.count}`);
          console.log(`- **Type**: ${r.implementation_type}`);
          console.log(`- **Best For**: ${r.best_for}`);
          console.log(`- **Docs**: ${r.docs_url}`);
          console.log(`- **CDN**: \`${r.cdn_url}\``);
          console.log('');
        }
      }
    } else {
      console.log(`\n# Top Icon Libraries (2025)\n`);
      console.log('| Name | Count | Type | Best For |');
      console.log('|---|---|---|---|');
      for (const r of records) {
        console.log(`| ${r.name} | ${r.count} | ${r.implementation_type} | ${r.best_for} |`);
      }
      console.log('\nRun `design-cli icons [name]` for details.\n');
    }

  } catch (err) {
    console.error(chalk.red('Failed to load icons:'), err);
  }
}
