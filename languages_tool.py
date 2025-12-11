#!/usr/bin/env python3
"""
Languages tool - Python version for extracting data from languages.yml
Works around V/prantlf.yaml memory issues with large files
"""

import sys
import yaml

def list_languages(yaml_file='languages.yml'):
    """List all languages with their native names"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    languages = []
    for key, lang_data in data['languages'].items():
        name = lang_data.get('name', '')
        native_name = lang_data.get('native_name', '')
        languages.append((name, native_name))

    # Sort by English name
    languages.sort(key=lambda x: x[0])

    for name, native_name in languages:
        if native_name:
            print(f"{name} ({native_name})")
        else:
            print(name)

def get_vocabulary(yaml_file='languages.yml', language_key=None):
    """Get vocabulary for a specific language"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if language_key not in data['languages']:
        print(f"Error: Language '{language_key}' not found")
        return

    lang = data['languages'][language_key]
    print(f"\n{lang['name']} ({lang.get('native_name', '')})")
    print("=" * 50)

    if 'vocabulary' in lang:
        for word, word_data in sorted(lang['vocabulary'].items()):
            primary = word_data.get('primary', '')
            native = word_data.get('scripts', {}).get('native', '')

            if native:
                print(f"{word.capitalize():15} {primary:20} ({native})")
            else:
                print(f"{word.capitalize():15} {primary}")
    else:
        print("No vocabulary data available")

def get_numbers(yaml_file='languages.yml', language_key=None):
    """Get numbers 0-10 for a specific language"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if language_key not in data['languages']:
        print(f"Error: Language '{language_key}' not found")
        return

    lang = data['languages'][language_key]
    print(f"\n{lang['name']} ({lang.get('native_name', '')})")
    print("=" * 50)

    if 'number_systems' in lang:
        for system_name, system_data in lang['number_systems'].items():
            if system_name != 'default' and system_data.get('name'):
                print(f"\n{system_data['name']}:")

            for num in range(11):
                num_str = str(num)
                if num_str in system_data.get('numbers', {}):
                    num_data = system_data['numbers'][num_str]
                    primary = num_data.get('primary', '')
                    scripts = num_data.get('scripts', {})

                    print(f"{num:2}: {primary:15}", end='')
                    if scripts:
                        native_script = ' / '.join([f"{v}" for k, v in scripts.items() if 'numeral' not in k])
                        if native_script:
                            print(f" ({native_script})", end='')
                    print()
    else:
        print("No number data available")

def main():
    if len(sys.argv) < 2:
        print("Usage: languages_tool.py <command> [language_key]")
        print("\nCommands:")
        print("  languages           - List all languages")
        print("  vocabulary <lang>   - Show vocabulary for language")
        print("  numbers <lang>      - Show numbers 0-10 for language")
        print("\nExample:")
        print("  languages_tool.py languages")
        print("  languages_tool.py vocabulary japanese")
        print("  languages_tool.py numbers hebrew")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'languages':
        list_languages()
    elif command == 'vocabulary':
        if len(sys.argv) < 3:
            print("Error: Please specify a language key")
            sys.exit(1)
        get_vocabulary(language_key=sys.argv[2])
    elif command == 'numbers':
        if len(sys.argv) < 3:
            print("Error: Please specify a language key")
            sys.exit(1)
        get_numbers(language_key=sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
