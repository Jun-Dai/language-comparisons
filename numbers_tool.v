// numbers_tool.v - Tool for extracting data from languages.yml
module main

import os
import prantlf.yaml { parse_file }

struct Language {
mut:
	key         string
	name        string
	native_name string
	family      string
	subfamily   string
}

struct NumbersData {
mut:
	languages map[string]Language
}

fn parse_yaml(path string) !NumbersData {
	// Parse the YAML file
	data := parse_file(path)!
	root := data.object()!

	// Get the languages section
	languages_any := root['languages']!
	languages_map := languages_any.object()!

	mut result := NumbersData{
		languages: map[string]Language{}
	}

	// Iterate through each language
	for key, lang_any in languages_map {
		lang_obj := lang_any.object()!

		mut lang := Language{
			key: key
		}

		// Extract language properties
		if name := lang_obj['name'] {
			lang.name = name.string()!
		}

		if native_name := lang_obj['native_name'] {
			lang.native_name = native_name.string()!
		}

		if family := lang_obj['family'] {
			lang.family = family.string()!
		}

		if subfamily := lang_obj['subfamily'] {
			lang.subfamily = subfamily.string()!
		}

		result.languages[key] = lang
	}

	return result
}

fn list_languages(data NumbersData) {
	// Collect and sort by English name
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
	yaml_path := 'languages.yml'

	data := parse_yaml(yaml_path) or {
		eprintln('Error parsing YAML: ${err}')
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
