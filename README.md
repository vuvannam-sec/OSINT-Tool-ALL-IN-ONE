# OSINT Tool All-in-One

A compact research toolkit for collecting, organizing, and visualizing publicly accessible Facebook data. The project combines a command-line launcher, browser-based crawlers, API helpers, and lightweight HTML visualizations in one repository.

This repository is maintained as an experimental OSINT project. Third-party endpoints and Facebook page structure change frequently, so individual collectors may require maintenance over time.

## What is included

- friend-layer collection from a Facebook account identifier;
- profile enrichment from previously collected data;
- optional RapidAPI helpers for profile, post, and comment metadata;
- friend-network visualization in `network.html`;
- check-in collection and route visualization;
- a small Flask API/server component used by parts of the local interface.

The main launcher is `PROJECT1report/source/new/run_all.py`.

## Repository layout

```text
PROJECT1report/source/new/
├── API/              # API-based profile/post/comment helpers
├── CrawCheckin/      # check-in collector and frontend
├── crawl/metaspy/    # browser-driven collection code
├── map/              # local visualization assets
├── api_server.py     # local Flask service
├── network.html      # relationship graph viewer
└── run_all.py        # interactive launcher
```

The `PROJECT1report` directory name is retained for compatibility with the existing project layout.

## Quick start

### Requirements

- Python 3.8+
- Node.js/npm for the check-in component
- Chrome/Chromium for browser-driven collectors

Create a virtual environment and install the Python dependencies used by the top-level application:

```bash
cd PROJECT1report/source/new
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
# .\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python run_all.py
```

Some nested components maintain their own dependencies. Install those from the component directory when using that feature.

## API configuration

Credentials are not stored in source code. RapidAPI-based helpers read the key from `RAPIDAPI_KEY`.

Linux/macOS:

```bash
export RAPIDAPI_KEY="your-key"
python run_all.py
```

PowerShell:

```powershell
$env:RAPIDAPI_KEY = "your-key"
python run_all.py
```

`.env.example` documents the expected variable name. Do not commit a populated `.env` file or paste credentials into Python source files.

## Data handling

Collectors can produce JSON files containing profile, post, comment, relationship, or location-derived information. Generated datasets should be treated as potentially sensitive even when the underlying source is public.

By default, generated API data, local environment files, caches, and dependency directories are excluded from version control. Review collected data before sharing it or attaching it to an issue.

## Responsible use

Use this project only on data you are legally permitted to access and in accordance with the relevant platform terms, local law, and research/organizational policy. Do not use it to bypass access controls, collect private-only content, or harass or target individuals.

The repository does not provide Facebook credentials, session cookies, or third-party API keys.

## Known limitations

- Facebook DOM/selectors and third-party API schemas can change without notice.
- Browser-driven features may require an authenticated local browser session.
- The current repository still contains legacy project structure that will be simplified incrementally rather than through a disruptive rewrite.
- Automated tests currently cover repository hygiene and syntax only; collector behavior still needs fixture-based tests.

## Development

Changes should keep secrets out of the repository, avoid committing generated datasets, and preserve the CLI workflow unless a migration is documented. See `CONTRIBUTING.md` and `SECURITY.md` before opening a pull request or reporting a sensitive issue.
