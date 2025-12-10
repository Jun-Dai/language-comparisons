// numbers_tool.v - Tool for extracting data from numbers.yml
module main

import os

struct Language {
mut:
	key             string
	name            string
	native_name     string
	alternate_names []string
	family          string
	subfamily       string
}

struct NumbersData {
mut:
	languages map[string]Language
}

fn parse_yaml(content string) !NumbersData {
	mut data := NumbersData{
		languages: map[string]Language{}
	}
	lines := content.split('\n')
	mut in_languages := false
	mut current_lang_key := ''
	mut current_lang := Language{}

	for line in lines {
		// Skip empty lines
		if line.trim_space() == '' {
			continue
		}

		// Check if we're in the languages section
		if line == 'languages:' {
			in_languages = true
			continue
		}

		if !in_languages {
			continue
		}

		// Detect language key (2 spaces indent, ends with colon)
		if line.starts_with('  ') && !line.starts_with('    ') && line.ends_with(':') {
			// Save previous language if exists
			if current_lang_key != '' {
				data.languages[current_lang_key] = current_lang
			}

			// Start new language
			current_lang_key = line.trim_space().trim_string_right(':')
			current_lang = Language{
				key: current_lang_key
			}
			continue
		}

		// Parse language properties (4 spaces indent)
		if line.starts_with('    ') && !line.starts_with('      ') {
			trimmed := line.trim_space()
			if trimmed.contains(':') {
				parts := trimmed.split(':')
				if parts.len >= 2 {
					key := parts[0].trim_space()
					value := parts[1..].join(':').trim_space().trim('"')

					match key {
						'name' {
							current_lang.name = value
						}
						'native_name' {
							current_lang.native_name = value
						}
						'family' {
							current_lang.family = value
						}
						'subfamily' {
							current_lang.subfamily = value
						}
						else {}
					}
				}
			}
		}
	}

	// Save last language
	if current_lang_key != '' {
		data.languages[current_lang_key] = current_lang
	}

	return data
}

fn read_yaml_file(path string) !NumbersData {
	content := os.read_file(path) or {
		return error('Failed to read file: ${err}')
	}
	return parse_yaml(content)
}

fn list_languages(data NumbersData) {
	// Collect and sort by English name instead of key
	mut lang_list := []Language{}
	for _, lang in data.languages {
		lang_list << lang
	}

	// Sort by name
	lang_list.sort(a.name < b.name)

	for lang in lang_list {
		if lang.name != '' {
			if lang.native_name != '' {
				println('${lang.name} (${lang.native_name})')
			} else {
				println('${lang.name}')
			}
		}
	}
}

fn main() {
	args := os.args[1..]

	if args.len == 0 {
		eprintln('Usage: numbers_tool <command>')
		eprintln('Commands:')
		eprintln('  languages  - List all languages in the file')
		exit(1)
	}

	command := args[0]
	yaml_path := 'numbers.yml'

	data := read_yaml_file(yaml_path) or {
		eprintln('Error reading YAML: ${err}')
		exit(1)
	}

	match command {
		'languages' {
			list_languages(data)
		}
		else {
			eprintln('Unknown command: ${command}')
			eprintln('Available commands: languages')
			exit(1)
		}
	}
}
