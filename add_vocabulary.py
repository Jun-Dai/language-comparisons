#!/usr/bin/env python3
"""
Parse new_words.txt and add vocabulary to languages.yml
"""

import re
import yaml

# Mapping from new_words.txt language names to languages.yml keys
LANG_NAME_TO_KEY = {
    'Adyghe': 'adyghe',
    'Ainu': 'ainu',
    'Albanian': 'albanian',
    'Amharic': 'amharic',
    'Arabic': 'arabic',
    'Aragonese': 'aragonese',
    'Basque': 'basque',
    'Belarussian': 'belarussian',
    'Brahui': 'brahui',
    'Cantonese': 'cantonese',
    'Catalan': 'catalan',
    'Czech': 'czech',
    'English': 'english',
    'Estonian': 'estonian',
    'Farsi': 'farsi',
    'Finnish': 'finnish',
    'French': 'french',
    'Galician': 'galician',
    'Georgian': 'georgian',
    'German': 'german',
    'Greek (ancient)': 'greek_ancient',
    'Greek (modern)': 'greek_modern',
    "Hawai'ian": 'hawaiian',
    'Hebrew': 'hebrew',
    'Hindi': 'hindi',
    'Hungarian': 'hungarian',
    'Indonesian': 'indonesian',
    'Italian': 'italian',
    'Japanese': 'japanese',
    'Kabardian': 'kabardian',
    'Latin': 'latin',
    'Latvian': 'latvian',
    'Lithuanian': 'lithuanian',
    "Ma'anyan": 'maanyan',
    'Malagasy': 'malagasy',
    'Malayalam': 'malayalam',
    'Maltese': 'maltese',
    'Mandarin': 'mandarin',
    'Māori': 'maori',
    'Northern Sami': 'northern_sami',
    'Pashto': 'pashto',
    'Portuguese': 'portuguese',
    'Romanian': 'romanian',
    'Russian': 'russian',
    'Slovak': 'slovak',
    'Southern Sami': 'southern_sami',
    'Spanish': 'spanish',
    'Tagalog': 'tagalog',
    'Taiwanese / Min Nan': 'taiwanese',
    'Tamil': 'tamil',
    'Telugu': 'telugu',
    'Tigrinya': 'tigrinya',
    'Uchinaaguchi': 'uchinaguchi',
    'Ukrainian': 'ukrainian',
    'Urdu': 'urdu',
}

def parse_vocabulary_file(filename):
    """Parse new_words.txt and return structured data"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    languages = {}
    current_lang = None

    for line in content.split('\n'):
        line = line.rstrip()

        # Check for language header
        if line.startswith('# '):
            lang_name = line[2:].strip()
            current_lang = lang_name
            if lang_name in LANG_NAME_TO_KEY:
                languages[LANG_NAME_TO_KEY[lang_name]] = {}
            continue

        # Skip empty lines and notes sections
        if not line or line.startswith('Notes on') or line.startswith('Important Notes') or line.startswith('Ainu colour') or line.startswith('(') or line.startswith('Ryukyuan') or line.startswith('All of these') or line.startswith('Most of these'):
            continue

        # Parse word entries (format: "Word: value")
        if ':' in line and current_lang and current_lang in LANG_NAME_TO_KEY:
            # Skip indented continuation lines
            if line.startswith('   '):
                continue

            # Split only on first colon
            parts = line.split(':', 1)
            if len(parts) == 2:
                word_key = parts[0].strip().lower().replace(' ', '_').replace("'", "")
                word_value = parts[1].strip()

                # Parse the value
                parsed = parse_word_value(word_value)
                lang_key = LANG_NAME_TO_KEY[current_lang]
                languages[lang_key][word_key] = parsed

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
        notes = notes.strip()
        while notes and notes[0] in '""\'"' and notes[-1] in '""\'"':
            notes = notes[1:-1].strip()
        result['notes'] = notes

    # Check for parentheses (scripts)
    paren_match = re.search(r'\(([^)]+)\)$', value)
    if paren_match:
        script_content = paren_match.group(1)
        value = value[:paren_match.start()].strip()
        result['scripts']['native'] = script_content

    # Check for alternates (with /)
    # Handle cases like "shtayim (f)" / "shnayim" properly
    value = value.strip()

    # Split by / but be careful about parentheses
    if '/' in value and '(' not in value.split('/')[0]:
        parts = [p.strip() for p in value.split('/')]
        result['primary'] = parts[0]
        result['alternates'] = parts[1:]
    else:
        result['primary'] = value

    return result

def add_vocabulary_to_yaml(yaml_file, vocab_file):
    """Add vocabulary entries to languages.yml"""

    # Parse vocabulary
    print("Parsing vocabulary from new_words.txt...")
    vocab_data = parse_vocabulary_file(vocab_file)

    # Read the YAML file
    print(f"Reading {yaml_file}...")
    with open(yaml_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Process each language by adding vocabulary section
    for lang_key, words in vocab_data.items():
        print(f"Adding vocabulary for {lang_key}...")

        # Find the language entry in the YAML
        # Look for the pattern "  lang_key:" followed by content and then either next language or end
        pattern = rf'(^  {re.escape(lang_key)}:.*?)(^  \w+:|\Z)'

        def add_vocab_section(match):
            lang_section = match.group(1)
            next_section = match.group(2)

            # Check if vocabulary section already exists
            if re.search(r'\n    vocabulary:', lang_section):
                print(f"  Warning: {lang_key} already has vocabulary section, skipping")
                return match.group(0)

            # Generate vocabulary YAML
            vocab_yaml = "\n    vocabulary:"
            for word_key in sorted(words.keys()):
                word_data = words[word_key]
                vocab_yaml += f"\n      {word_key}:"

                # Escape quotes in primary value
                primary = word_data['primary'].replace('"', '\\"').replace("'", "''")
                vocab_yaml += f'\n        primary: "{primary}"'

                if word_data['alternates']:
                    alts = ', '.join([f'"{a.replace(chr(34), chr(92)+chr(34))}"' for a in word_data['alternates']])
                    vocab_yaml += f'\n        alternates: [{alts}]'

                if word_data['scripts']:
                    vocab_yaml += f'\n        scripts:'
                    for script_type, script_value in word_data['scripts'].items():
                        script_value = script_value.replace('"', '\\"')
                        vocab_yaml += f'\n          {script_type}: "{script_value}"'

                if word_data['notes']:
                    notes = word_data['notes'].replace('"', '\\"')
                    vocab_yaml += f'\n        notes: "{notes}"'

            vocab_yaml += "\n"

            # Insert vocabulary before the next language or at the end
            return lang_section + vocab_yaml + next_section

        content = re.sub(pattern, add_vocab_section, content, flags=re.MULTILINE | re.DOTALL)

    # Write back the updated YAML
    print(f"Writing updated {yaml_file}...")
    with open(yaml_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Done!")

if __name__ == '__main__':
    add_vocabulary_to_yaml(
        '/home/user/language-comparisons/languages.yml',
        '/home/user/language-comparisons/new_words.txt'
    )
