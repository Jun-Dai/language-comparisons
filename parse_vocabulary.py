#!/usr/bin/env python3
"""
Parse new_words.txt and generate YAML vocabulary entries for languages.yml
"""

import re
import sys

def parse_vocabulary_file(filename):
    """Parse new_words.txt and return structured data"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by language headers (lines starting with #)
    languages = {}
    current_lang = None

    for line in content.split('\n'):
        line = line.rstrip()

        # Check for language header
        if line.startswith('# '):
            lang_name = line[2:].strip()
            current_lang = lang_name
            languages[lang_name] = {}
            continue

        # Skip empty lines and notes sections
        if not line or line.startswith('Notes on') or line.startswith('Important Notes') or line.startswith('Ainu colour') or line.startswith('(') or line.startswith('Ryukyuan'):
            continue

        # Parse word entries (format: "Word: value")
        if ':' in line and current_lang:
            # Split only on first colon
            parts = line.split(':', 1)
            if len(parts) == 2:
                word_key = parts[0].strip().lower()
                word_value = parts[1].strip()

                # Skip if this is a continuation line (indented)
                if line.startswith('   '):
                    continue

                # Parse the value
                parsed = parse_word_value(word_value)
                languages[current_lang][word_key] = parsed

    return languages

def parse_word_value(value):
    """Parse a word value into components: primary, alternates, scripts, notes"""
    result = {
        'primary': '',
        'alternates': [],
        'scripts': {},
        'notes': ''
    }

    # Check for notes (after ←)
    if '←' in value:
        value, notes = value.split('←', 1)
        # Remove quotes and extra whitespace
        notes = notes.strip()
        # Remove surrounding quotes if present
        while notes and notes[0] in '""\'"' and notes[-1] in '""\'"':
            notes = notes[1:-1].strip()
        result['notes'] = notes

    # Check for parentheses (scripts)
    paren_match = re.search(r'\(([^)]+)\)', value)
    if paren_match:
        script_content = paren_match.group(1)
        # Remove the parenthetical content from value
        value = value[:paren_match.start()].strip() + ' ' + value[paren_match.end():].strip()
        value = value.strip()

        # Store the script
        result['scripts']['native'] = script_content

    # Check for alternates (with /)
    if '/' in value:
        parts = [p.strip() for p in value.split('/')]
        result['primary'] = parts[0]
        result['alternates'] = parts[1:]
    else:
        result['primary'] = value.strip()

    return result

def generate_yaml_vocabulary(languages_data):
    """Generate YAML vocabulary sections for each language"""

    for lang_name, words in sorted(languages_data.items()):
        print(f"\n# ========== {lang_name} ==========")
        print("    vocabulary:")

        for word_key, word_data in sorted(words.items()):
            print(f"      {word_key}:")
            print(f"        primary: \"{word_data['primary']}\"")

            if word_data['alternates']:
                alts = ', '.join([f'"{a}"' for a in word_data['alternates']])
                print(f"        alternates: [{alts}]")

            if word_data['scripts']:
                print(f"        scripts:")
                for script_type, script_value in word_data['scripts'].items():
                    print(f"          {script_type}: \"{script_value}\"")

            if word_data['notes']:
                print(f"        notes: \"{word_data['notes']}\"")

if __name__ == '__main__':
    languages_data = parse_vocabulary_file('/home/user/language-comparisons/new_words.txt')
    generate_yaml_vocabulary(languages_data)
