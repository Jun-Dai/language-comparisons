# Language Comparisons - Numbers and Vocabulary Across Languages

A comprehensive database of numbers 0-10 and core vocabulary (31 words) in 55 languages, organized by language family, with support for multiple writing systems and number systems.

## Overview

This project catalogs numbers from different languages to explore linguistic relationships and patterns. The hypothesis: it's fairly easy to tell how closely or distantly related two languages are by comparing how they say numbers 1-9.

## Current Languages

The database includes **55 languages** from these language families:
- **Indo-European**: Hindi, Urdu, Farsi, Pashto, English, German, Latin, Romance languages (French, Spanish, Italian, Portuguese, Romanian, Catalan, Aragonese, Galician), Greek (Modern & Ancient), Albanian, Slavic languages (Russian, Ukrainian, Belarusian, Czech, Slovak), Baltic languages (Latvian, Lithuanian)
- **Dravidian**: Tamil, Telugu, Malayalam, Brahui
- **Uralic**: Hungarian, Estonian, Finnish, Northern Sami, Southern Sami
- **Afro-Asiatic (Semitic)**: Arabic, Hebrew, Maltese, Amharic, Tigrinya
- **Austronesian**: Indonesian, Tagalog, Ma'anyan, Malagasy, Māori, Hawaiian
- **Sino-Tibetan**: Cantonese, Mandarin, Taiwanese/Min Nan
- **Japonic**: Japanese, Uchinaguchi (Okinawan)
- **Kartvelian**: Georgian
- **Northwest Caucasian**: Adyghe, Kabardian
- **Language Isolates**: Ainu, Basque

## Data Format

The data is stored in `languages.yml` with the following structure:

```yaml
languages:
  <language_key>:
    name: "Language Name"
    alternate_names: ["Alt Name 1", "Alt Name 2"]
    family: "Language Family"
    subfamily: "Subfamily"
    notes: |
      Notes about the language and its number system
    number_systems:
      <system_name>:
        name: "System Name (optional)"
        notes: "System-specific notes (optional)"
        numbers:
          "0":
            primary: "romanization"
            alternates: ["alternate1", "alternate2"]
            scripts:
              script_name: "native script"
              script_name_numeral: "native numeral"
          "1":
            primary: "romanization"
            scripts:
              script_name: "native script"
          # ... through 10
    vocabulary:
      mother:
        primary: "romanization"
        scripts:
          native: "native script"
      father:
        primary: "romanization"
        alternates: ["alternate form"]
        scripts:
          native: "native script"
        notes: "optional notes"
      # ... 31 vocabulary words total
    references:
      - "URL 1"
      - "URL 2"
```

### Vocabulary Words

Each language includes 31 core vocabulary words:
- **Family**: mother, father, man, woman, child, grandmother
- **Basic**: name, food, soup, bread
- **Places**: house, bridge
- **Nature**: sun, moon, cloud, rain, water, fire, stone, tree
- **Body**: tooth, nose, eye
- **Animals**: bird, fish
- **Colors**: green, red, yellow, blue, black, white

## Setup Instructions (macOS)

### Prerequisites

- macOS 10.13 or later
- Xcode Command Line Tools
- Git

### Installing Command Line Tools

If you don't have Xcode Command Line Tools installed:

```bash
xcode-select --install
```

### Installing V (Vlang)

The extraction tool is written in V. To install V on macOS:

**Option 1: Using Homebrew (Recommended)**
```bash
brew install vlang
```

**Option 2: Build from Source**
```bash
# Clone V repository
git clone https://github.com/vlang/v
cd v

# Build V
make

# Add V to your PATH (add this to your ~/.zshrc or ~/.bash_profile)
export PATH="$PATH:/path/to/v"

# Or create a symlink
sudo ln -s /path/to/v/v /usr/local/bin/v
```

**Option 3: Using V's installer script**
```bash
curl -o install.sh https://raw.githubusercontent.com/vlang/v/master/cmd/tools/install.vsh
chmod +x install.sh
./install.sh
```

### Verify Installation

```bash
v version
```

You should see output like: `V 0.4.x xxxxx`

## Using the Numbers Tool

### Clone the Repository

```bash
git clone https://github.com/Jun-Dai/language-comparisons.git
cd language-comparisons
```

### Install Dependencies

The tool uses the `prantlf.yaml` library for YAML parsing. Install the required modules:

```bash
# Install YAML parser
v install --git https://github.com/prantlf/v-yaml

# Install jany (required dependency for yaml)
v install --git https://github.com/prantlf/v-jany

# Set up proper module structure
mkdir -p ~/.vmodules/prantlf
ln -sf ~/.vmodules/prantlf.yaml ~/.vmodules/prantlf/yaml
ln -sf ~/.vmodules/prantlf.jany ~/.vmodules/prantlf/jany
```

### Run Commands

#### List All Languages

```bash
v run numbers_tool.v languages
```

This will output all languages in the database:
```
adyghe: Adyghe
ainu: Ainu
albanian: Albanian
...
```

#### Build the Tool (Optional)

For faster execution, you can compile the tool:

```bash
v numbers_tool.v -o numbers_tool
./numbers_tool languages
```

The compiled binary will run significantly faster than using `v run` each time.

### Available Commands

Currently implemented:
- `languages` - List all languages in the database

Coming soon:
- More extraction and reporting commands

## Development

### File Structure

```
language-comparisons/
├── README.md              # This file
├── languages.yml          # Main data file (numbers + vocabulary)
├── new_words.txt          # Source vocabulary data
├── numbers_page.mediawiki # Original mediawiki source for numbers
├── numbers_tool.v         # V extraction tool
├── add_vocabulary.py      # Python script to integrate vocabulary
└── parse_vocabulary.py    # Python vocabulary parser
```

### Known Issues

⚠️ **V Tool Memory Issue**: The `numbers_tool.v` currently has memory issues with the larger `languages.yml` file (184KB, 8000+ lines) due to limitations in the prantlf.yaml library. The YAML file itself is valid and can be parsed with standard YAML libraries (Python, Ruby, etc.). We're working on a solution for the V tool or may provide alternative Python-based tools.

### Adding New Languages

1. Add the language data to `languages.yml` following the schema above
2. Include all available writing systems (romanization, native scripts, numerals)
3. Add both numbers (0-10) and vocabulary (31 words)
4. Add references for your sources
5. Commit and push your changes

### Modifying the Tool

The tool is written in V and designed to be easily extensible. To add new commands:

1. Open `numbers_tool.v`
2. Add your command function
3. Add a match case in the `main()` function
4. Test with `v run numbers_tool.v <your_command>`

## Contributing

Contributions are welcome! You can help by:
- Adding new languages
- Correcting errors in existing data
- Adding additional metadata (IPA, audio links, etc.)
- Improving the extraction tool
- Adding new report formats

## License

[To be determined]

## References

Key sources used for this project:
- [Omniglot - Numbers in various languages](https://omniglot.com/language/numbers/)
- [Languages and Numbers](https://www.languagesandnumbers.com/)
- [Wikipedia - List of numbers in various languages](https://en.wikipedia.org/wiki/List_of_numbers_in_various_languages)
- Individual language references listed in `languages.yml`

## Acknowledgments

Original data compilation by Jun-Dai from Wikipedia user page:
[User:Jun-Dai/Linguistics/Numbers_1–10](https://en.wikipedia.org/wiki/User:Jun-Dai/Linguistics/Numbers_1%E2%80%9310)
