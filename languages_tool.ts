#!/usr/bin/env tsx
/**
 * Languages tool - TypeScript version for extracting data from languages.yml
 * Works around V/prantlf.yaml memory issues with large files
 */

import { readFileSync } from 'fs';
import { parse } from 'yaml';

interface Scripts {
  [key: string]: string;
}

interface WordData {
  primary: string;
  alternates?: string[];
  scripts?: Scripts;
  notes?: string;
}

interface NumberData {
  primary: string;
  alternates?: string[];
  scripts?: Scripts;
}

interface NumberSystem {
  name?: string;
  numbers: {
    [key: string]: NumberData;
  };
}

interface Language {
  name: string;
  native_name?: string;
  family: string;
  subfamily?: string;
  notes?: string;
  number_systems?: {
    [key: string]: NumberSystem;
  };
  vocabulary?: {
    [key: string]: WordData;
  };
  references?: string[];
}

interface LanguagesData {
  languages: {
    [key: string]: Language;
  };
}

function loadLanguages(yamlFile: string = 'languages.yml'): LanguagesData {
  const content = readFileSync(yamlFile, 'utf-8');
  return parse(content) as LanguagesData;
}

function listLanguages(data: LanguagesData): void {
  const languages = Object.entries(data.languages).map(([key, lang]) => ({
    key,
    name: lang.name,
    nativeName: lang.native_name || '',
  }));

  // Sort by English name
  languages.sort((a, b) => a.name.localeCompare(b.name));

  for (const lang of languages) {
    if (lang.nativeName) {
      console.log(`${lang.name} (${lang.nativeName})`);
    } else {
      console.log(lang.name);
    }
  }
}

function getVocabulary(data: LanguagesData, languageKey: string): void {
  const lang = data.languages[languageKey];

  if (!lang) {
    console.error(`Error: Language '${languageKey}' not found`);
    process.exit(1);
  }

  console.log(`\n${lang.name} (${lang.native_name || ''})`);
  console.log('='.repeat(50));

  if (!lang.vocabulary) {
    console.log('No vocabulary data available');
    return;
  }

  const words = Object.entries(lang.vocabulary).sort(([a], [b]) =>
    a.localeCompare(b)
  );

  for (const [word, wordData] of words) {
    const primary = wordData.primary || '';
    const native = wordData.scripts?.native || '';
    const capitalize = word.charAt(0).toUpperCase() + word.slice(1);

    if (native) {
      console.log(`${capitalize.padEnd(15)} ${primary.padEnd(20)} (${native})`);
    } else {
      console.log(`${capitalize.padEnd(15)} ${primary}`);
    }
  }
}

function getNumbers(data: LanguagesData, languageKey: string): void {
  const lang = data.languages[languageKey];

  if (!lang) {
    console.error(`Error: Language '${languageKey}' not found`);
    process.exit(1);
  }

  console.log(`\n${lang.name} (${lang.native_name || ''})`);
  console.log('='.repeat(50));

  if (!lang.number_systems) {
    console.log('No number data available');
    return;
  }

  for (const [systemName, system] of Object.entries(lang.number_systems)) {
    if (systemName !== 'default' && system.name) {
      console.log(`\n${system.name}:`);
    }

    for (let num = 0; num <= 10; num++) {
      const numStr = num.toString();
      const numData = system.numbers[numStr];

      if (numData) {
        const primary = numData.primary || '';
        process.stdout.write(`${num.toString().padStart(2)}: ${primary.padEnd(15)}`);

        if (numData.scripts) {
          const nativeScripts = Object.entries(numData.scripts)
            .filter(([key]) => !key.includes('numeral'))
            .map(([, value]) => value);

          if (nativeScripts.length > 0) {
            process.stdout.write(` (${nativeScripts.join(' / ')})`);
          }
        }
        console.log();
      }
    }
  }
}

function main(): void {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: languages_tool.ts <command> [language_key]');
    console.log('\nCommands:');
    console.log('  languages           - List all languages');
    console.log('  vocabulary <lang>   - Show vocabulary for language');
    console.log('  numbers <lang>      - Show numbers 0-10 for language');
    console.log('\nExample:');
    console.log('  tsx languages_tool.ts languages');
    console.log('  tsx languages_tool.ts vocabulary japanese');
    console.log('  tsx languages_tool.ts numbers hebrew');
    process.exit(1);
  }

  const command = args[0];
  const data = loadLanguages();

  switch (command) {
    case 'languages':
      listLanguages(data);
      break;

    case 'vocabulary':
      if (args.length < 2) {
        console.error('Error: Please specify a language key');
        process.exit(1);
      }
      getVocabulary(data, args[1]);
      break;

    case 'numbers':
      if (args.length < 2) {
        console.error('Error: Please specify a language key');
        process.exit(1);
      }
      getNumbers(data, args[1]);
      break;

    default:
      console.error(`Unknown command: ${command}`);
      process.exit(1);
  }
}

main();
