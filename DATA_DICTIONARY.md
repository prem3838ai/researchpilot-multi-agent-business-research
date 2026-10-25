# Data dictionary

`data/demo_sources.json` contains illustrative source-like records used only to demonstrate the application workflow.

| Field | Meaning |
|---|---|
| `id` | Stable evidence identifier (e.g. S1) |
| `title` | Illustrative title with `{topic}` placeholder |
| `snippet` | Illustrative research snippet, not a verified factual claim |
| `url` | In demo mode generated placeholder URL on `example.com` |

Live search records are normalized into `id`, `title`, `url`, `snippet`, `published_date`, and `demo` fields.
