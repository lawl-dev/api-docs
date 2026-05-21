# Vended `/v3/languages` responses

This directory holds verbatim JSON responses from the DeepL `/v3/languages` endpoints, fetched against `https://api.deepl.com`. Other tooling in this repo (e.g. generated docs and snippets) reads these files instead of calling the API directly.

## Files

| File | Endpoint |
|---|---|
| `resources.json` | `GET /v3/languages/resources` |
| `<resource>.json` | `GET /v3/languages?resource=<resource>&include=beta&include=external` |

where <resource> is one of the resources returned by `/resources` (`translate_text`, `translate_document`,
`voice`, `write`, etc.).

Each per-resource file requests `include=beta&include=external` so the vended data is the full superset. Consumers filter on the `status` and per-feature `external` fields when they want a narrower view.

These files are refreshed hourly by the [`refresh-v3-languages`](../../.github/workflows/refresh-v3-languages.yml) GitHub Action, which runs [`scripts/fetch_v3_languages.py`](../../scripts/fetch_v3_languages.py) and opens a pull request whenever the API responses change. See that script's module docstring or `--help` for flags and behaviour (auth, alternate endpoints, manual local refresh).

## `translation_memory.json`

Translation Memory is not yet exposed by `/v3/languages`, so `translation_memory.json` is currently maintained by hand in the shape of a `/v3/languages` response. The fetcher skips it; once the API exposes Translation Memory as a resource, the next refresh will overwrite the manual file with the real response and no other code has to change.
