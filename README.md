# Tech Department Career Framework

A statically generated documentation site for a tech department career framework using SFIA (Skills Framework for the Information Age) skill definitions.

## Overview

This repository contains:

- SFIA skill definitions (CSV format)
- Scripts to parse SFIA data and generate role pages
- MkDocs configuration for building a browseable documentation site
- Generated markdown documentation for each role at each level

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Setup

### 1. Create a Virtual Environment

It's recommended to use a virtual environment to avoid installing packages globally:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

This will install:
- `mkdocs` - Static site generator
- `mkdocs-material` - Material theme for MkDocs
- `pandas` - Data processing for CSV parsing

### 3. Generate Role Pages

Generate all role pages from the SFIA CSV data:

```bash
# Make sure you're in the repository root
cd /path/to/skills

# Run the generation script
python scripts/generate_pages.py
```

This will create markdown files in the `docs/roles/` directory for all roles.

### 4. Preview the Documentation

Start the MkDocs development server with **hot reload** enabled:

**Option 1: Using the dev script (recommended)**
```bash
# Using the shell script
./dev.sh

# Or using the Python script
python dev.py
```

**Option 2: Using mkdocs directly**
```bash
mkdocs serve --livereload
```

Then open your browser to `http://127.0.0.1:8000` to preview the documentation.

**Hot Reload:** The development server automatically watches for changes in your markdown files and reloads the page in your browser when you save changes. No need to manually refresh!

### 5. Build the Static Site

Generate the static HTML site:

```bash
mkdocs build
```

The generated site will be in the `site/` directory.

## Project Structure

```
skills/
├── input/
│   └── sfia-9_current-standard_en_250129(Skills).csv  # SFIA skill definitions
├── scripts/
│   ├── parse_sfia.py          # Parse CSV and extract skill data
│   └── generate_pages.py      # Generate markdown role pages
├── docs/
│   ├── index.md               # Landing page
│   ├── about.md               # About SFIA and the framework
│   └── roles/                 # Generated role pages (created by script)
│       ├── engineering/
│       ├── management/
│       ├── product/
│       └── programmes/
├── mkdocs.yml                 # MkDocs configuration
├── requirements.txt           # Python dependencies
├── dev.sh                     # Development server script (hot reload)
├── dev.py                     # Development server script (Python)
└── README.md                  # This file
```

## Role Definitions

### Engineering Roles

Five engineering tracks, each with 7 levels (Levels 1-7):

- **Software Engineer**: SWDN, PROG, ARCH, DBAD, DEPL
- **Security Engineer**: IRMG, SCTY, PENT
- **Support Engineer**: CSMG, ASUP, INCA
- **Systems Engineer**: SYSP, CHMG, ITOP, ASMG, DEMM, DCMA, USUP
- **QA Engineer**: TEST, NFTS, QUAS, BPTS

### Management Roles

Levels 4-7:

- **People Management**: ETMG, POMG, SORC, SUPP

### Product Roles

Levels 3-7:

- **Product Management**: PROD, REQM, BSMO, CEXP, DEMG

### Programmes Roles

Levels 2-6:

- **Programme Management**: POMG (and others as defined)

## Customizing Roles

To modify role definitions or add new roles:

1. Edit `scripts/generate_pages.py`
2. Update the `ROLE_SKILLS` dictionary with skill codes for each role
3. Update the `ROLE_TITLES` dictionary with role titles
4. Regenerate pages: `python scripts/generate_pages.py`

## Development

### Development Server with Hot Reload

The development server includes **hot reload** functionality. When you edit any markdown file in the `docs/` directory, the browser will automatically refresh to show your changes.

Start the dev server:
```bash
./dev.sh
# or
python dev.py
# or
mkdocs serve --livereload
```

The server watches for changes and automatically reloads the page. This makes editing and previewing documentation much faster!

### Testing the Parser

Test the SFIA CSV parser:

```bash
python scripts/parse_sfia.py
```

This will parse the CSV and display example skills.

### Regenerating Pages

After making changes to role definitions or the SFIA data:

```bash
python scripts/generate_pages.py
```

If the dev server is running, it will automatically detect the changes and reload. Otherwise, rebuild the site:

```bash
mkdocs build
```

## Deployment

The static site in the `site/` directory can be deployed to any static hosting service:

- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any web server

## Troubleshooting

### Virtual Environment Issues

If you encounter issues with the virtual environment:

```bash
# Deactivate current environment
deactivate

# Remove and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### CSV Parsing Errors

If the CSV parser fails:

1. Check that the CSV file exists in `input/`
2. Verify the file encoding (the script tries multiple encodings)
3. Check for CSV format issues

### Missing Skills

If a skill code is not found:

1. Verify the skill code exists in the SFIA CSV
2. Check the spelling/case of the skill code
3. The script will warn about missing skills but continue

## License

This framework uses SFIA skill definitions. Please refer to SFIA licensing for use of SFIA content.

## Contributing

To contribute improvements:

1. Make changes to scripts or documentation
2. Test locally with `mkdocs serve`
3. Regenerate pages if role definitions changed
4. Submit changes for review
